# Pluto AI: Intelligent Agent Framework and NBA Prediction Model

**Pluto AI** is an AI-driven project designed to explore the power of reasoning and collaborative decision-making through agents. The project features a library called **Agency**, which serves as a framework for building intelligent agents. Pluto AI ( the impl. of agency framework ) uses this framework to model and predict outcomes of NBA team games based on team-specific data. Pluto AI is a 3b llama3.2 uncescored model fine tuned on data from the Los Angeles Lakers and also given a persoanlity to make takes/predictions more relatable.

---

## **Features**
- **Agency Library**: A reusable framework for creating AI agents with built-in reasoning and feedback mechanisms.
- **Pluto AI Model**: An AI agent trained on specific NBA team data to predict game outcomes.
- **Collaborative Reasoning**: Agents interact with a centralized reasoning engine, providing feedback to ensure decisions are refined before final approval.
- **Async Execution**: Fully asynchronous architecture for scalable and efficient task execution.

---

## **How It Works**

### **Agency Library**
The **Agency** library enables the creation of AI agents that:
1. **Plan Tasks**: A reasoning engine determines an action plan for agents based on the given prompt.
2. **Execute Tasks**: Agents execute the action plan using their specialized tools.
3. **Provide Feedback**: Agents report results to the reasoning engine, which evaluates and provides feedback.
4. **Iterate for Refinement**: The process iterates until the reasoning engine approves the final result.

## **Future Developments**
1. Impl. a scheduler inside agency lib that will better orchestrate when agents should be running, a step toward autonomy.

### **Pluto AI**
Pluto AI uses the **Agency** framework to:
1. Analyze NBA team data, such as player performance, game strategies, and historical trends.
2. Predict outcomes of specific team games.
3. Generate insights with a collaborative reasoning approach to enhance accuracy.
4. Predicts individual player stat lines.

---
