"""Gradio interface for the Career Advisor app."""

import logging

import gradio as gr

from career_advisor.pipeline import full_pipeline
from career_advisor.preferences import (
    init_preferences_file,
    load_personalization_preferences,
)


logger = logging.getLogger(__name__)


def run_pipeline_for_ui(
    user_profile,
    chosen_role,
    resume_file,
    session_state,
    mode,
    learning_style,
    career_goals,
):
    logger.info("Submit clicked.")
    if not user_profile or not user_profile.strip():
        logger.info("Empty profile submitted; stopping.")
        yield "⚠️ Please add your profile/description before submitting.", session_state
        return

    logger.info("Running career advisor pipeline with mode=%r.", mode)
    yield (
        "⏳ Running the career advisor pipeline...\n\n"
        "The first run can take a few minutes in Colab while the open-source model "
        "and embeddings are downloaded and loaded.",
        session_state,
    )

    try:
        result_markdown, new_state = full_pipeline(
            user_profile=user_profile,
            chosen_role=chosen_role,
            resume_file=resume_file,
            mode=mode,
            learning_style=learning_style,
            career_goals=career_goals,
        )
    except Exception as exc:
        logger.exception("Pipeline error.")
        yield f"❌ Pipeline error:\n\n```text\n{exc}\n```", session_state
        return

    logger.info("Pipeline completed.")
    yield result_markdown, new_state


def toggle_personalization_fields(mode):
    show = mode == "personalized"
    if show:
        learning_style, career_goals = load_personalization_preferences()
        return gr.update(visible=True, value=learning_style), gr.update(
            visible=True, value=career_goals
        )
    return gr.update(visible=False), gr.update(visible=False)


def clear_form():
    return "", "", None, "default", gr.update(visible=False), gr.update(visible=False), "", None


init_preferences_file()
default_learning_style, default_career_goals = load_personalization_preferences()

with gr.Blocks(css=".gr-button { width: 100% !important; }") as demo:
    output_md = gr.Markdown(label="📊 Αποτελέσματα")

    profile = gr.Textbox(lines=8, label="🔍 Προφίλ / Περιγραφή", interactive=True)
    role = gr.Textbox(lines=1, label="🎯 Επιλεγμένος Ρόλος (προαιρετικά)", interactive=True)
    resume = gr.File(label="📄 Βιογραφικό (PDF)", file_types=[".pdf"])
    mode_dropdown = gr.Dropdown(
        ["default", "interview", "personalized"],
        label="Λειτουργία",
        value="default",
    )
    learning_style_input = gr.Dropdown(
        choices=["visual", "auditory", "hands-on"],
        label="📚 Στυλ Μάθησης",
        value=default_learning_style,
        visible=False,
    )
    career_goals_input = gr.Textbox(
        label="🎯 Στόχοι Καριέρας",
        value=default_career_goals,
        visible=False,
    )

    mode_dropdown.change(
        toggle_personalization_fields,
        inputs=[mode_dropdown],
        outputs=[learning_style_input, career_goals_input],
    )

    state = gr.State()
    submit_btn = gr.Button("🚀 Submit")
    clear_btn = gr.Button("🧹 Clear")

    submit_btn.click(
        fn=run_pipeline_for_ui,
        inputs=[
            profile,
            role,
            resume,
            state,
            mode_dropdown,
            learning_style_input,
            career_goals_input,
        ],
        outputs=[output_md, state],
    )

    clear_btn.click(
        fn=clear_form,
        outputs=[
            profile,
            role,
            resume,
            mode_dropdown,
            learning_style_input,
            career_goals_input,
            output_md,
            state,
        ],
    )


demo.queue(default_concurrency_limit=1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demo.launch(share=False, debug=False)
