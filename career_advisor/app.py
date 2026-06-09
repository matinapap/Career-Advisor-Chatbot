"""Gradio interface for the Career Advisor app."""

import gradio as gr

from career_advisor.pipeline import full_pipeline
from career_advisor.preferences import (
    init_preferences_file,
    load_personalization_preferences,
)


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
        fn=full_pipeline,
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


if __name__ == "__main__":
    demo.launch(share=False, debug=False)
