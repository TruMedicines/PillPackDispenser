from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter

app = Flask(__name__)
skill_builder = SkillBuilder()
# Register your intent handlers to the skill_builder object

skill_adapter = SkillAdapter( skill=skill_builder.create(), skill_id='amzn1.ask.skill.25ce4d0a-0206-4ea1-86a3-876f2ebcfc81', app=app)

@app.route("/")
def invoke_skill():
    return skill_adapter.dispatch_request()

if __name__ == '__main__':
    app.run()
