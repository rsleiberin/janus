from flask import Blueprint, jsonify, request
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.routes.errors import handle_route_error
from backend.db import db
from backend.models import Analytics

# Initialize blueprint and logger
analytics_bp = Blueprint("analytics", __name__)
logger = CentralizedLogger("analytics_routes")


@analytics_bp.route("/analytics", methods=["POST"])
def create_analytics_record():
    """
    Endpoint to create a new analytics record.
    """
    try:
        logger.log_to_console("INFO", "Creating a new analytics record.")
        data = request.json
        if not data or "data" not in data:
            raise ValueError("Invalid payload: 'data' is required.")
        
        research_topic = data.get("research_topic", "General")
        analytics_record = Analytics(data=data["data"], research_topic=research_topic)
        db.session.add(analytics_record)
        db.session.commit()

        logger.log_to_console("INFO", "Analytics record created successfully.")
        return jsonify({"message": "Analytics record created successfully."}), 201

    except Exception as e:
        return handle_route_error(e)


@analytics_bp.route("/analytics", methods=["GET"])
def get_analytics_records():
    """
    Endpoint to fetch all analytics records.
    """
    try:
        logger.log_to_console("INFO", "Fetching all analytics records.")
        records = Analytics.query.all()
        serialized_records = [
            {
                "id": record.id,
                "data": record.data,
                "research_topic": record.research_topic,
                "created_at": record.created_at,
            }
            for record in records
        ]

        logger.log_to_console("INFO", f"Fetched {len(serialized_records)} analytics records.")
        return jsonify(serialized_records), 200

    except Exception as e:
        return handle_route_error(e)


@analytics_bp.route("/analytics/<int:record_id>", methods=["DELETE"])
def delete_analytics_record(record_id):
    """
    Endpoint to delete an analytics record by ID.
    """
    try:
        logger.log_to_console("INFO", f"Deleting analytics record with ID: {record_id}.")
        record = Analytics.query.get(record_id)
        if not record:
            raise ValueError(f"Analytics record with ID {record_id} not found.")

        db.session.delete(record)
        db.session.commit()

        logger.log_to_console("INFO", f"Analytics record {record_id} deleted successfully.")
        return jsonify({"message": f"Analytics record {record_id} deleted successfully."}), 200

    except Exception as e:
        return handle_route_error(e)


# Future Expansion
# Consider adding system monitoring features, including CPU, memory, and disk usage metrics.
# Evaluate psutil or alternative libraries before implementation.
# These features will require dedicated helper functions and schema updates if needed.
