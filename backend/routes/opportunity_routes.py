from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from extensions import db

from models.opportunity import Opportunity

from utils.validators import VALID_CATEGORIES

opportunity_bp = Blueprint("opportunity", __name__)


@opportunity_bp.route("", methods=["GET"])
@jwt_required()
def get_opportunities():

    user_id = get_jwt_identity()

    opportunities = Opportunity.query.filter_by(
        admin_id=user_id
    ).order_by(
        Opportunity.created_at.desc()
    ).all()

    if not opportunities:
        return jsonify({
            "opportunities": [],
            "message": "No opportunities found"
        }), 200

    return jsonify({
        "opportunities": [
            opportunity.to_dict()
            for opportunity in opportunities
        ]
    })


@opportunity_bp.route("", methods=["POST"])
@jwt_required()
def create_opportunity():

    user_id = get_jwt_identity()

    data = request.get_json()

    required_fields = [
        "name",
        "duration",
        "start_date",
        "description",
        "skills",
        "category",
        "future_opportunities"
    ]

    for field in required_fields:

        if not data.get(field):
            return jsonify({
                "message": f"{field} is required"
            }), 400


    category = data.get("category").strip().lower()
    valid_categories = [
        c.lower() for c in VALID_CATEGORIES
    ]

    if category not in valid_categories:

        return jsonify({
            "message": "Invalid category"
        }), 400
    
    max_applicants = data.get("max_applicants")

    if max_applicants == "":
        max_applicants = None

    new_opportunity = Opportunity(
        name=data.get("name"),
        duration=data.get("duration"),
        start_date=data.get("start_date"),
        description=data.get("description"),
        skills=data.get("skills"),
        category=data.get("category"),
        future_opportunities=data.get("future_opportunities"),
        prerequisites=data.get("prerequisites"),
        max_applicants=max_applicants,
        admin_id=user_id
    )

    db.session.add(new_opportunity)

    db.session.commit()

    return jsonify({
        "message": "Opportunity created successfully",
        "opportunity": new_opportunity.to_dict()
    }), 201


@opportunity_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_single_opportunity(id):

    user_id = get_jwt_identity()

    opportunity = Opportunity.query.get(id)

    if not opportunity:
        return jsonify({
            "message": "Opportunity not found"
        }), 404

    if str(opportunity.admin_id) != str(user_id):
        return jsonify({
            "message": "Unauthorized"
        }), 403

    return jsonify(opportunity.to_dict())


@opportunity_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_opportunity(id):

    user_id = get_jwt_identity()

    opportunity = Opportunity.query.get(id)

    if not opportunity:
        return jsonify({
            "message": "Opportunity not found"
        }), 404

    if str(opportunity.admin_id) != str(user_id):
        return jsonify({
            "message": "Unauthorized"
        }), 403

    data = request.get_json()

    required_fields = [
        "name",
        "duration",
        "start_date",
        "description",
        "skills",
        "category",
        "future_opportunities"
    ]

    for field in required_fields:

        if not data.get(field):
            return jsonify({
                "message": f"{field} is required"
            }), 400

    category = data.get("category").strip().lower()

    valid_categories = [
        c.lower() for c in VALID_CATEGORIES
    ]

    if category not in valid_categories:

        return jsonify({
            "message": "Invalid category"
        }), 400
    
    max_applicants = data.get("max_applicants")

    if max_applicants == "":
        max_applicants = None

    opportunity.name = data.get("name")
    opportunity.duration = data.get("duration")
    opportunity.start_date = data.get("start_date")
    opportunity.description = data.get("description")
    opportunity.skills = data.get("skills")
    opportunity.category = data.get("category")
    opportunity.future_opportunities = data.get("future_opportunities")
    opportunity.prerequisites = data.get("prerequisites")
    opportunity.max_applicants = max_applicants

    db.session.commit()

    return jsonify({
        "message": "Opportunity updated successfully",
        "opportunity": opportunity.to_dict()
    }), 200


@opportunity_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_opportunity(id):

    user_id = get_jwt_identity()

    opportunity = Opportunity.query.get(id)

    if not opportunity:
        return jsonify({
            "message": "Opportunity not found"
        }), 404

    if str(opportunity.admin_id) != str(user_id):
        return jsonify({
            "message": "Unauthorized"
        }), 403

    db.session.delete(opportunity)

    db.session.commit()

    return jsonify({
        "message": "Opportunity deleted successfully"
    }), 200