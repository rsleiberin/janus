import pytest
import logging
from backend.db import db
from backend.db.helpers.analytics_helpers import AnalyticsHelpers
from backend.models import Analytics

# Configure console logging for test suite
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("test_logger")


@pytest.mark.usefixtures("function_db_setup")
def test_create_analytics():
    """
    Tests the creation of an Analytics record using AnalyticsHelpers.create_analytics.
    """
    logger.debug("Starting test_create_analytics...")

    sample_data = {"field": "value", "nested": {"key": 123}}
    analytics = AnalyticsHelpers.create_analytics(session=db.session, data=sample_data)
    logger.debug("[CREATE_ANALYTICS] Analytics created: %s", analytics)

    assert analytics.id is not None, "Analytics entry was not assigned an ID."
    assert analytics.data == sample_data, "Analytics data mismatch."
    logger.debug("test_create_analytics passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_id():
    """
    Tests retrieval of an Analytics record by its ID.
    """
    logger.debug("Starting test_get_by_id...")

    sample_data = {"test": "get_by_id"}
    analytics = AnalyticsHelpers.create_analytics(session=db.session, data=sample_data)
    db.session.flush()  # Ensure the new analytics is written to DB

    fetched_analytics = AnalyticsHelpers.get_by_id(session=db.session, analytics_id=analytics.id)
    logger.debug("[GET_BY_ID] Fetched analytics: %s", fetched_analytics)

    assert fetched_analytics is not None, "Fetched analytics is None, expected a valid record."
    assert fetched_analytics.id == analytics.id, "Fetched ID does not match created analytics."
    logger.debug("test_get_by_id passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_all_analytics():
    """
    Tests retrieving all Analytics records.
    """
    logger.debug("Starting test_get_all_analytics...")

    sample_data_1 = {"field1": "abc"}
    sample_data_2 = {"field2": "xyz"}
    AnalyticsHelpers.create_analytics(session=db.session, data=sample_data_1)
    AnalyticsHelpers.create_analytics(session=db.session, data=sample_data_2)

    all_analytics = AnalyticsHelpers.get_all_analytics(session=db.session)
    logger.debug("[GET_ALL_ANALYTICS] Fetched analytics list: %s", all_analytics)

    assert len(all_analytics) == 2, f"Expected 2 analytics entries, found {len(all_analytics)}."
    logger.debug("test_get_all_analytics passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_recent_analytics():
    """
    Tests retrieving the most recent Analytics records with a limit.
    """
    logger.debug("Starting test_get_recent_analytics...")

    # Create multiple entries
    for i in range(5):
        AnalyticsHelpers.create_analytics(session=db.session, data={"index": i})

    # We ask for the 3 most recent
    recent_entries = AnalyticsHelpers.get_recent_analytics(session=db.session, limit=3)
    logger.debug("[GET_RECENT_ANALYTICS] Recent entries: %s", recent_entries)

    assert len(recent_entries) == 3, f"Expected 3 most recent entries, found {len(recent_entries)}."
    logger.debug("test_get_recent_analytics passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_delete_analytics():
    """
    Tests deleting an Analytics record by ID.
    """
    logger.debug("Starting test_delete_analytics...")

    sample_data = {"delete": True}
    analytics = AnalyticsHelpers.create_analytics(session=db.session, data=sample_data)
    logger.debug("[DELETE_ANALYTICS] Created analytics: %s", analytics)

    AnalyticsHelpers.delete_analytics(session=db.session, analytics_id=analytics.id)
    logger.debug("[DELETE_ANALYTICS] Analytics deleted.")

    deleted_entry = AnalyticsHelpers.get_by_id(session=db.session, analytics_id=analytics.id)
    logger.debug("[DELETE_ANALYTICS] Deleted entry: %s", deleted_entry)

    assert deleted_entry is None, "Analytics record still present after deletion."
    logger.debug("test_delete_analytics passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_count_analytics():
    """
    Tests counting the total number of Analytics records.
    """
    logger.debug("Starting test_count_analytics...")

    data1 = {"test": "count1"}
    data2 = {"test": "count2"}
    AnalyticsHelpers.create_analytics(session=db.session, data=data1)
    AnalyticsHelpers.create_analytics(session=db.session, data=data2)

    count = AnalyticsHelpers.count(session=db.session)
    logger.debug("[COUNT_ANALYTICS] Count: %d", count)

    assert count == 2, f"Expected 2 analytics records, found {count}"
    logger.debug("test_count_analytics passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_exists_analytics():
    """
    Tests whether an Analytics record exists by ID.
    """
    logger.debug("Starting test_exists_analytics...")

    sample_data = {"exists_check": True}
    analytics = AnalyticsHelpers.create_analytics(session=db.session, data=sample_data)
    logger.debug("[EXISTS_ANALYTICS] Created analytics: %s", analytics)

    exists = AnalyticsHelpers.exists(session=db.session, analytics_id=analytics.id)
    logger.debug("[EXISTS_ANALYTICS] Exists result: %s", exists)

    assert exists is True, "Expected analytics to exist, but got False."
    logger.debug("test_exists_analytics passed successfully.")
