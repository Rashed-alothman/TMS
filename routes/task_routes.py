# routes/task_routes.py
# Handles all REST API endpoints for tasks.
# Each function here does ONE thing: receive a request, call logic, return JSON.

import logging
from datetime import datetime

from flask import Blueprint, jsonify, request
from models.database import Task, db
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

# A Blueprint is like a mini-app. We register it in app.py.
# The url_prefix means every route here starts with /homepage/api/tasks
task_api = Blueprint("task_api", __name__, url_prefix="/homepage/api/tasks")

# --- Reusable error messages ---
ERR_INVALID_DATA = "Invalid or missing data"
ERR_UNEXPECTED = "An unexpected error occurred"
ERR_DATABASE = "Database error occurred"


@task_api.route("", methods=["GET"])
def get_tasks():
    """Return all tasks, with optional filtering and sorting."""
    try:
        completed_param = request.args.get("completed")
        priority_param = request.args.get("priority")
        sort_by = request.args.get("sort", "created_at")

        query = Task.query

        if completed_param is not None:
            completed_bool = completed_param.lower() == "true"
            query = query.filter_by(completed=completed_bool)

        if priority_param:
            query = query.filter_by(priority=priority_param)

        if sort_by == "created_at":
            query = query.order_by(Task.created_at.desc())
        elif sort_by == "due_date":
            query = query.order_by(Task.due_date.asc().nullslast())
        elif sort_by == "priority":
            priority_order = ["urgent", "high", "medium", "low"]
            query = query.order_by(
                db.case(
                    {p: i for i, p in enumerate(priority_order)}, value=Task.priority
                )
            )

        tasks = query.all()
        return jsonify({"Tasks": [task.to_dict() for task in tasks]})

    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching tasks: {str(e)}")
        return jsonify({"error": ERR_DATABASE}), 500
    except Exception as e:
        logger.error(f"Unexpected error while fetching tasks: {str(e)}")
        return jsonify({"error": ERR_UNEXPECTED}), 500


@task_api.route("/add_tasks", methods=["POST"])
def add_task():
    """Create a new task."""
    try:
        data = request.get_json()

        if not data or "description" not in data:
            return jsonify({"error": ERR_INVALID_DATA}), 400

        priority = data.get("priority", "low").lower()
        valid_priorities = ["low", "medium", "high", "urgent"]

        if priority not in valid_priorities:
            return jsonify(
                {"error": f"Priority must be one of: {valid_priorities}"}
            ), 400

        new_task = Task(
            description=data["description"], due_date=datetime.now(), priority=priority
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Task added", "task": new_task.to_dict()}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error while adding task: {str(e)}")
        return jsonify({"error": ERR_DATABASE}), 500
    except Exception as e:
        logger.error(f"Unexpected error while adding task: {str(e)}")
        return jsonify({"error": ERR_UNEXPECTED}), 500


@task_api.route("/delete_task", methods=["DELETE"])
def delete_task():
    """Delete a task by ID."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": ERR_INVALID_DATA}), 400

        task_id = data.get("id")
        if not task_id:
            return jsonify({"error": "Task ID is required"}), 400

        task = Task.query.filter_by(id=task_id).first()
        if not task:
            return jsonify({"message": "Task not found"}), 404

        db.session.delete(task)
        db.session.commit()
        logger.info(f"Task deleted: {task_id}")
        return jsonify({"message": "Task deleted successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error while deleting task: {str(e)}")
        return jsonify({"error": ERR_DATABASE}), 500
    except Exception as e:
        logger.error(f"Unexpected error while deleting task: {str(e)}")
        return jsonify({"error": ERR_UNEXPECTED}), 500


@task_api.route("/update_task", methods=["PATCH"])
def update_task():
    """Update a task's description or completion status."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": ERR_INVALID_DATA}), 400

        task_id = data.get("id")
        if not task_id:
            return jsonify({"error": "Task ID is required"}), 400

        task = Task.query.filter_by(id=task_id).first()
        if not task:
            return jsonify({"message": "Task not found"}), 404

        if data.get("description") is not None:
            task.description = data["description"]
        if data.get("completed") is not None:
            task.completed = data["completed"]

        db.session.commit()
        return jsonify({"message": "Task updated", "task": task.to_dict()}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error while updating task: {str(e)}")
        return jsonify({"error": ERR_DATABASE}), 500
    except Exception as e:
        logger.error(f"Unexpected error while updating task: {str(e)}")
        return jsonify({"error": ERR_UNEXPECTED}), 500
