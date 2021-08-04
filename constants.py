from auto_editor.AddCommentsRule import AddCommentsRule
from auto_editor.AddCommentsTestRule import AddCommentsTestRule
from auto_editor.Fix1003Rule import Fix1003Rule
from auto_editor.Fix1049Rule import Fix1049Rule

RULES_TO_DESCRIPTIONS = {
    Fix1003Rule: "Improve DPCT exception handling to simplify code",
    Fix1049Rule: "Reproduce 1049 manual changes from sample data",
    AddCommentsRule: "Insert comments to provide recommendations for various warnings",
    AddCommentsTestRule: "Insert comments to provide recommendations for various warnings"
}
