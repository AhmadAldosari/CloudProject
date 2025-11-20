"""Application routes and view logic."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, redirect, render_template, request, url_for, flash

from app.extensions import db
from app.models import InventoryItem

bp = Blueprint("dashboard", __name__)


@bp.route("/health", methods=["GET"])
def health() -> tuple[dict, int]:
    """Health check consumed by Elastic Load Balancing."""
    return jsonify(status="ok"), 200


@bp.route("/", methods=["GET", "POST"])
def dashboard():
    """Render the dashboard and handle item creation."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        quantity_raw = request.form.get("quantity", "0").strip()
        price_raw = request.form.get("price", "0").strip()

        if not name:
            flash("Item name is required.", "danger")
        else:
            try:
                quantity = int(quantity_raw)
            except ValueError:
                flash("Quantity must be an integer.", "danger")
            else:
                try:
                    price = Decimal(price_raw)
                except (InvalidOperation, ValueError):
                    flash("Price must be a valid number.", "danger")
                else:
                    item = InventoryItem(name=name, quantity=quantity, price=price)
                    db.session.add(item)
                    db.session.commit()
                    flash(f"Added '{name}' to inventory.", "success")
                    return redirect(url_for("dashboard.dashboard"))

    items = InventoryItem.query.order_by(InventoryItem.created_at.desc()).all()
    return render_template("dashboard.html", items=items)


@bp.post("/delete/<int:item_id>")
def delete_item(item_id: int):
    """Delete an inventory item and redirect back to the dashboard."""
    item = InventoryItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f"Deleted '{item.name}' from inventory.", "info")
    return redirect(url_for("dashboard.dashboard"))
