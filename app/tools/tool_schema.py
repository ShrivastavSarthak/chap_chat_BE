from app.tools.time_tool import get_current_time

TOOL_SCHEMA = [
    {
        "type": "function",
        "name": "get_current_time",
        "description": "Returns the current UTC date and time.",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone_name": {
                    "type": "string",
                    "description": "The timezone requested by the user, e.g. IST or UTC",
                }
            },
            "required": ["timezone_name"],
            "additionalProperties": False,
        },
    },
]


TOOL_EXECUTION = {
    "get_current_time": get_current_time
}