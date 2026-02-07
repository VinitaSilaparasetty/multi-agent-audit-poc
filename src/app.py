
@app.route("/process", methods=["POST"])def process():

    config = {"configurable": {"thread_id": "audit_demo_001"}}

    # This will run 'shop' and then PAUSE before 'order'

    app.invoke({"query": "laptop", "audit_trail": []}, config)

    return "AI suggests Laptop. Waiting for human approval..."@app.route("/approve", methods=["POST"])def approve():

    config = {"configurable": {"thread_id": "audit_demo_001"}}

    # Update state with human approval and RESUME

    app.update_state(config, {"is_approved": True, "selected_product": "Standard Laptop"})

    app.invoke(None, config)

    return "Compliance verified. Order placed."

