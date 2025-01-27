import pytest
from unittest.mock import patch
from backend.db import db
from backend.db.helpers.analytics_helpers import AnalyticsHelpers


@pytest.mark.usefixtures("function_db_setup")
def test_create_analytics():
    sample_data = {"field": "value", "nested": {"key": 123}}
    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log, patch(
        "backend.utils.logger.CentralizedLogger.log_to_db"
    ) as mock_db_log:
        analytics = AnalyticsHelpers.create_analytics(session=db.session, data=sample_data)

        assert analytics.id is not None, "Analytics entry was not assigned an ID."
        assert analytics.data == sample_data, "Analytics data mismatch."

        mock_console_log.assert_called_with("INFO", "Analytics entry created", meta_data={"data": sample_data})
        mock_db_log.assert_called_with(
            level="INFO",
            message="Analytics entry created",
            module="analytics_helpers",
            meta_data={"data": sample_data},
        )


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_id():
    sample_data = {"test": "get_by_id"}
    analytics = AnalyticsHelpers.create_analytics(session=db.session, data=sample_data)

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log:
        fetched_analytics = AnalyticsHelpers.get_by_id(session=db.session, analytics_id=analytics.id)

        assert fetched_analytics is not None, "Fetched analytics is None."
        assert fetched_analytics.id == analytics.id, "Fetched ID does not match created analytics."

        mock_console_log.assert_called_with(
            "INFO", f"Retrieved analytics entry by ID: {analytics.id}", meta_data={"found": True}
        )

    with pytest.raises(ValueError, match=f"Analytics entry with ID 9999 not found."):
        AnalyticsHelpers.get_by_id(session=db.session, analytics_id=9999)


@pytest.mark.usefixtures("function_db_setup")
def test_get_all_analytics():
    sample_data_1 = {"field1": "abc"}
    sample_data_2 = {"field2": "xyz"}
    AnalyticsHelpers.create_analytics(session=db.session, data=sample_data_1)
    AnalyticsHelpers.create_analytics(session=db.session, data=sample_data_2)

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log:
        all_analytics = AnalyticsHelpers.get_all_analytics(session=db.session)

        assert len(all_analytics) == 2, f"Expected 2 analytics entries, found {len(all_analytics)}."
        mock_console_log.assert_called_with("INFO", "Retrieved all analytics entries", meta_data={"count": 2})


@pytest.mark.usefixtures("function_db_setup")
def test_delete_analytics():
    sample_data = {"delete": True}
    analytics = AnalyticsHelpers.create_analytics(session=db.session, data=sample_data)

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log:
        AnalyticsHelpers.delete_analytics(session=db.session, analytics_id=analytics.id)

        with pytest.raises(ValueError, match=f"Analytics entry with ID {analytics.id} not found."):
            AnalyticsHelpers.get_by_id(session=db.session, analytics_id=analytics.id)

        mock_console_log.assert_any_call("INFO", f"Deleted analytics entry with ID: {analytics.id}")


@pytest.mark.usefixtures("function_db_setup")
def test_count_analytics():
    data1 = {"test": "count1"}
    data2 = {"test": "count2"}
    AnalyticsHelpers.create_analytics(session=db.session, data=data1)
    AnalyticsHelpers.create_analytics(session=db.session, data=data2)

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log:
        count = AnalyticsHelpers.count(session=db.session)

        assert count == 2, f"Expected 2 analytics records, found {count}"
        mock_console_log.assert_called_with("INFO", "Total analytics entries count retrieved", meta_data={"count": 2})


@pytest.mark.usefixtures("function_db_setup")
def test_exists_analytics():
    sample_data = {"exists_check": True}
    analytics = AnalyticsHelpers.create_analytics(session=db.session, data=sample_data)

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_console_log:
        exists = AnalyticsHelpers.exists(session=db.session, analytics_id=analytics.id)

        assert exists is True, "Expected analytics to exist, but got False."
        mock_console_log.assert_called_with(
            "INFO",
            f"Analytics entry existence check for ID: {analytics.id}",
            meta_data={"exists": True},
        )
