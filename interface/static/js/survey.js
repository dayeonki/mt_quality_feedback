function agg_screen(i, notes){
    survey_text = ''

    highlight_question = '<div style="margin-top:10px;margin-bottom:20px">\
            <p>The highlights were useful. I feel that highlights helped in determining whether the translated text contained an accuracy error.</p>\
            <div style="margin-left:40px; marign-top:10px">\
                <input type="radio" id="h_1" name="h'+i+'" value="1">\
                <label for="h_1" style="margin-right:10px; margin-left:5px; font-weight: normal;">Strongly Disagree</label>\
                <input type="radio" id="h_2" name="h'+i+'" value="2">\
                <label for="h_2" style="margin-right:10px; margin-left:5px; font-weight: normal;">Disagree</label>\
                <input type="radio" id="h_3" name="h'+i+'" value="3">\
                <label for="h_3" style="margin-right:10px; margin-left:5px; font-weight: normal;">Neutral</label>\
                <input type="radio" id="h_4" name="h'+i+'" value="4">\
                <label for="h_4" style="margin-right:10px; margin-left:5px; font-weight: normal;">Agree</label>\
                <input type="radio" id="h_5" name="h'+i+'" value="5">\
                <label for="h_5" style="margin-right:10px; margin-left:5px; font-weight: normal;">Strongly Agree</label>\
            </div>\
        </div>'



        confidenceSelf_question = '<div style="margin-top:10px;margin-bottom:20px">\
            <p>I am confident in my decisions.</p>\
            <div style="margin-left:40px; marign-top:10px">\
                <input type="radio" id="r_1" name="r'+i+'" value="1">\
                <label for="r_1" style="margin-right:10px; margin-left:5px; font-weight: normal;">Strongly Disagree</label>\
                <input type="radio" id="r_2" name="r'+i+'" value="2">\
                <label for="r_2" style="margin-right:10px; margin-left:5px; font-weight: normal;">Disagree</label>\
                <input type="radio" id="r_3" name="r'+i+'" value="3">\
                <label for="r_3" style="margin-right:10px; margin-left:5px; font-weight: normal;">Neutral</label>\
                <input type="radio" id="r_4" name="r'+i+'" value="4">\
                <label for="r_4" style="margin-right:10px; margin-left:5px; font-weight: normal;">Agree</label>\
                <input type="radio" id="r_5" name="r'+i+'" value="5">\
                <label for="r_5" style="margin-right:10px; margin-left:5px; font-weight: normal;">Strongly Agree</label>\
            </div>\
        </div>'

        likeToUse_question = '<div style="margin-top:10px;margin-bottom:20px">\
            <p>I would like to use the AI system to help me detect accuracy errors in AI-generated translations.</p>\
            <div style="margin-left:40px; marign-top:10px">\
                <input type="radio" id="l_1" name="l'+i+'" value="1">\
                <label for="l_1" style="margin-right:10px; margin-left:5px; font-weight: normal;">Strongly Disagree</label>\
                <input type="radio" id="l_2" name="l'+i+'" value="2">\
                <label for="l_2" style="margin-right:10px; margin-left:5px; font-weight: normal;">Disagree</label>\
                <input type="radio" id="l_3" name="l'+i+'" value="3">\
                <label for="l_3" style="margin-right:10px; margin-left:5px; font-weight: normal;">Neutral</label>\
                <input type="radio" id="l_4" name="l'+i+'" value="4">\
                <label for="l_4" style="margin-right:10px; margin-left:5px; font-weight: normal;">Agree</label>\
                <input type="radio" id="l_5" name="l'+i+'" value="5">\
                <label for="l_5" style="margin-right:10px; margin-left:5px; font-weight: normal;">Strongly Agree</label>\
            </div>\
        </div>'

        if (w_hl==false){
            highlight_question = ''
        }

        survey_text += '<div class="panel panel-primary">\
            <div class="panel-heading">\
                <div><strong>Please indicate whether your agree or disagree with each of the statements below.</strong> </div>\
            </div>\
            <div class="task">\
                <div class="row">\
                    <div class="col-md-7">'
                    + highlight_question + confidenceSelf_question + likeToUse_question +
                    '</div>\
                    <div class="col-md-1">\
                    </div>\
                    <div class="col-md-3">\
                        <div style="margin-top:20px;">Add your feedback here.</div>\
                        <input type="text" class="form-control" name="notes'+i+'" id="notes'+i+'" rows="5" value=""></input> \
                    </div>\
                </div>\
            </div>\
        </div>'
    $(survey_text).appendTo('#task_screen'+i)
}