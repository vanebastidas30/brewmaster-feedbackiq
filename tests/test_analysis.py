from src.analysis.prompts import analysis_prompt, summary_prompt

def test_analysis_prompt_structure():

    text = "El café estaba delicioso"
    prompt = analysis_prompt(text, 5)

    assert "sentiment" in prompt
    assert "categories" in prompt
    assert "urgency" in prompt


def test_report_prompt_structure():

    prompt = summary_prompt(
        total=100,
        sentiment={"positive": 60},
        top_locations=[(1, 4.5)],
        problem_locations=[(2, 10)],
        categories=[("servicio", 20)]
    )

    assert "resumen ejecutivo" in prompt.lower()
    assert "Total de reseñas" in prompt