from fastapi.testclient import TestClient

import routers.api as api_router_module
from main import app
from schemas import LearningPathResponse, LearningPathStep, QuizQuestion, QuizResponse


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_qa(monkeypatch):
    monkeypatch.setattr(
        api_router_module,
        "answer_question",
        lambda text: "The Pacific Ocean is the largest ocean.",
    )
    response = client.post("/qa", json={"question": "Which is the largest ocean?"})
    assert response.status_code == 200
    assert "Pacific" in response.json()["answer"]


def test_quiz(monkeypatch):
    quiz = QuizResponse(
        title="Water Cycle",
        questions=[
            QuizQuestion(
                question="What happens after evaporation?",
                options=["Condensation", "Collection", "Freezing", "Melting"],
                correct_answer="Condensation",
                explanation="Water vapor cools and condenses into droplets.",
            ),
            QuizQuestion(
                question="What is precipitation?",
                options=["Rain or snow falling", "Water heating", "Cloud formation only", "Ocean currents"],
                correct_answer="Rain or snow falling",
                explanation="Precipitation is water falling from clouds.",
            ),
            QuizQuestion(
                question="Where can collected water be found?",
                options=["Rivers and lakes", "Only clouds", "Only deserts", "Only glaciers"],
                correct_answer="Rivers and lakes",
                explanation="Collection occurs in bodies such as rivers and lakes.",
            ),
        ],
    )
    monkeypatch.setattr(api_router_module, "generate_quiz", lambda text: quiz)

    response = client.post("/quiz", json={"text": "Water cycle passage"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["questions"]) == 3
    assert all(len(q["options"]) == 4 for q in data["questions"])


def test_learning_path(monkeypatch):
    path = LearningPathResponse(
        topic="SQL",
        learner_level="beginner",
        duration="8 weeks",
        steps=[
            LearningPathStep(
                stage="Foundations",
                topics=["Tables", "Rows", "SELECT"],
                estimated_time="2 weeks",
                resources=["SQL documentation"],
                practice=["Write SELECT queries"],
            )
        ],
    )
    monkeypatch.setattr(
        api_router_module,
        "get_learning_recommendations",
        lambda topic, level, weeks: path,
    )

    response = client.post(
        "/learn/recommendations",
        json={"topic": "SQL", "level": "beginner", "weeks": 8},
    )
    assert response.status_code == 200
    assert response.json()["topic"] == "SQL"


def test_empty_input_is_rejected():
    response = client.post("/qa", json={"text": "   "})
    assert response.status_code == 422
