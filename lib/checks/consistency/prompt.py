CONSISTENCY_CHECK_TEMPLATE = """\
        INSTRUCTIONS:
        You are judging whether a statement about a message is consistent or inconsistent.

        Your goal is to give a point value to the statement, where 1 is very consistent, -1 is very contradictory, and 0 is unsure or unrelated. 
        How extreme your point value is determines how confident you are in your judgment.

        Think through it step-by-step, then write down your reasoning. Finally, give a point value to the statement.

        Make sure the judgment is a float between -1 and 1, and the output is a valid XML document.

        INPUT FORMAT:
        <input>
            <message>The message to judge</message>
            <statement>The statement to judge.</statement>
        </input>

        OUTPUT FORMAT:
        <response>
            <input>
                <message>The message to judge</message>
                <statement>The statement to judge</statement>
            </input>
            <reasoning>The reasoning for the judgment</reasoning>
            <judgment>The judgment to give the statement</judgment>
        </response>

        EXAMPLES:
        <response>
            <input>
                <message>I like dogs.</message>
                <statement>The speaker likes dogs.</statement>
            </input>
            <reasoning>Because the message and the statement both assert the speaker likes dogs, the statement is very consistent with the message, so the score is 1.</reasoning>
            <judgment>1.0</judgment>
        </response>
        
        <response>
            <input>
                <message>I like dogs.</message>
                <statement>The doesn't likes dogs.</statement>
            </input>
            <reasoning>Because the statement directly contradicts the message, the statement is very inconsistent, so the score should be -1.</reasoning>
            <judgment>-1.0</judgment>
        </response>
        
        <response>
            <input>
                <message>I like dogs.</message>
                <statement>The speaker likes cats.</statement>
            </input>
            <reasoning>It's not clear whether the speaker does or does not like cats based on the message, so the statement is unrelated, so the score is 0.</reasoning>
            <judgment>0.0</judgment>
        </response>

        Make sure the judgment is a float between -1 and 1, and the output is a valid XML document.

        TASK:
        <input>
            <message>{message}</message>
            <statement>{statement}</statement>
        <input>

        OUTPUT:
    """