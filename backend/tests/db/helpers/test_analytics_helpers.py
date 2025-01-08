import pytest
from unittest.mock import patch
from backend.db import db
from backend.db.helpers.analytics_helpers import AnalyticsHelpers
from backend.utils.error_handling.db.errors import AnalyticsNotFoundError


@pytest.mark.usefixtures("function_db_setup")
def test_create_analytics():
    """
    Tests the creation of an Analytics record using AnalyticsHelpers.create_analytics.
    """
    sample_data = {"field": "value", "nested": {"key": 123}}
    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log, \
         patch("backend.utils.logger.CentralizedLogger.log_to_db") as mock_db_log:
        analytics = AnalyticsHelpers.create_analytics(session=db.session, data=sample_data)

        # Verify creation
        assert analytics.id is not None, "Analytics entry was not assigned an ID."
        assert analytics.data == sample_data, "Analytics data mismatch."

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO",
            "Analytics entry created",
            data=sample_data
        )
        mock_db_log.assert_called_with(
            level="INFO",
            message="Analytics entry created",
            module="analytics_helpers",
            meta_data={"data": sample_data}
        )


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_id():
    """
    Tests retrieval of an Analytics record by its ID.
    """
    sample_data = {"test": "get_by_id"}
    analytics = AnalyticsHelpers.create_analytics(session=db.session, data=sample_data)

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log, \
         patch("backend.utils.logger.CentralizedLogger.log_to_db") as mock_db_log:
        fetched_analytics = AnalyticsHelpers.get_by_id(session=db.session, analytics_id=analytics.id)

        # Verify retrieval
        assert fetched_analytics is not None, "Fetched analytics is None, expected a valid record."
        assert fetched_analytics.id == analytics.id, "Fetched ID does not match created analytics."

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO",
            f"Retrieved analytics entry by ID: {analytics.id}",
            found=True
        )
        mock_db_log.assert_called_with(
            level="INFO",
            message=f"Retrieved analytics entry by ID: {analytics.id}",
            module="analytics_helpers",
            meta_data={"analytics_id": analytics.id, "found": True}
        )


@pytest.mark.usefixtures("function_db_setup")
def test_get_all_analytics():
    """
    Tests retrieving all Analytics records.
    """
    sample_data_1 = {"field1": "abc"}
    sample_data_2 = {"field2": "xyz"}
    AnalyticsHelpers.create_analytics(session=db.session, data=sample_data_1)
    AnalyticsHelpers.create_analytics(session=db.session, data=sample_data_2)

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log, \
         patch("backend.utils.logger.CentralizedLogger.log_to_db") as mock_db_log:
        all_analytics = AnalyticsHelpers.get_all_analytics(session=db.session)

        # Verify retrieval
        assert len(all_analytics) == 2, f"Expected 2 analytics entries, found {len(all_analytics)}."

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO",
            "Retrieved all analytics entries",
            count=2
        )
        mock_db_log.assert_called_with(
            level="INFO",
            message="Retrieved all analytics entries",
            module="analytics_helpers",
            meta_data={"count": 2}
        )


@pytest.mark.usefixtures("function_db_setup")
def test_get_recent_analytics():
    """
    Tests retrieving the most recent Analytics records with a limit.
    """
    for i in range(5):
        AnalyticsHelpers.create_analytics(session=db.session, data={"index": i})

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log, \
         patch("backend.utils.logger.CentralizedLogger.log_to_db") as mock_db_log:
        recent_entries = AnalyticsHelpers.get_recent_analytics(session=db.session, limit=3)

        # Verify retrieval
        assert len(recent_entries) == 3, f"Expected 3 most recent entries, found {len(recent_entries)}."

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO",
            "Retrieved recent analytics entries (limit 3)",
            count=3
        )
        mock_db_log.assert_called_with(
            level="INFO",
            message="Retrieved recent analytics entries (limit 3)",
            module="analytics_helpers",
            meta_data={"limit": 3, "count": 3}
        )


@pytest.mark.usefixtures("function_db_setup")
def test_delete_analytics():
    """
    Tests deleting an Analytics record by ID.
    """
    sample_data = {"delete": True}
    analytics = AnalyticsHelpers.create_analytics(session=db.session, data=sample_data)

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log, \
         patch("backend.utils.logger.CentralizedLogger.log_to_db") as mock_db_log:
        AnalyticsHelpers.delete_analytics(session=db.session, analytics_id=analytics.id)

        # Verify deletion by asserting that get_by_id raises AnalyticsNotFoundError
        with pytest.raises(AnalyticsNotFoundError, match=f"Analytics entry with ID {analytics.id} not found."):
            AnalyticsHelpers.get_by_id(session=db.session, analytics_id=analytics.id)

        # Verify logging for console
        mock_console_log.assert_any_call(
            "INFO",
            f"Deleted analytics entry with ID: {analytics.id}"
        )

        # Verify logging for database
        mock_db_log.assert_any_call(
            level="INFO",
            message=f"Deleted analytics entry with ID: {analytics.id}",
            module="analytics_helpers",
            meta_data={"analytics_id": analytics.id}
        )

@pytest.mark.usefixtures("function_db_setup")
def test_count_analytics():
    """
    Tests counting the total number of Analytics records.
    """
    data1 = {"test": "count1"}
    data2 = {"test": "count2"}
    AnalyticsHelpers.create_analytics(session=db.session, data=data1)
    AnalyticsHelpers.create_analytics(session=db.session, data=data2)

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log, \
         patch("backend.utils.logger.CentralizedLogger.log_to_db") as mock_db_log:
        count = AnalyticsHelpers.count(session=db.session)

        # Verify count
        assert count == 2, f"Expected 2 analytics records, found {count}"

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO",
            "Total analytics entries count retrieved",
            count=2
        )
        mock_db_log.assert_called_with(
            level="INFO",
            message="Total analytics entries count retrieved",
            module="analytics_helpers",
            meta_data={"count": 2}
        )


@pytest.mark.usefixtures("function_db_setup")
def test_exists_analytics():
    """
    Tests whether an Analytics record exists by ID.
    """
    sample_data = {"exists_check": True}
    analytics = AnalyticsHelpers.create_analytics(session=db.session, data=sample_data)

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log, \
         patch("backend.utils.logger.CentralizedLogger.log_to_db") as mock_db_log:
        exists = AnalyticsHelpers.exists(session=db.session, analytics_id=analytics.id)

        # Verify existence check
        assert exists is True, "Expected analytics to exist, but got False."

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO",
            f"Analytics entry existence check for ID: {analytics.id}",
            exists=True
        )
        mock_db_log.assert_called_with(
            level="INFO",
            message=f"Analytics entry existence check for ID: {analytics.id}",
            module="analytics_helpers",
            meta_data={"analytics_id": analytics.id, "exists": True}
        )
