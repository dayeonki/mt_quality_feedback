const display_source = (Counter, textDiv, text) => {
    highlighted_text = highlight(text)
    if(w_hl==false){
        highlighted_text = highlighted_text.replace('<h-l-1>', '')
        highlighted_text = highlighted_text.replace('</h-l-1>', '')
        highlighted_text = highlighted_text.replace('<h-l-2>', '')
        highlighted_text = highlighted_text.replace('</h-l-2>', '')
        highlighted_text = highlighted_text.replace('<h-l-3>', '')
        highlighted_text = highlighted_text.replace('</h-l-3>', '')
        highlighted_text = highlighted_text.replace('<h-l-4>', '')
        highlighted_text = highlighted_text.replace('</h-l-4>', '')
    }
    $('<div>'+highlighted_text+'</div>').appendTo(textDiv)
    return Promise.resolve('display_source completed')
}


const load_source = (Counter) => {
    var textDiv = $('#text_screen' + taskCounter)
    var fg_idx = taskCounter;
    var sample = sample_indices[fg_idx-1]
    return fetch('static/examples/'+examples_dir+'/src_' + sample + '.txt')
        .then(response => response.text())
        .then(text => display_source(Counter, textDiv, text))
}


function display_target(Counter, textDiv, text){
    highlighted_text = highlight(text)
    if(w_hl==false){
        highlighted_text = highlighted_text.replace('<h-l-1>', '')
        highlighted_text = highlighted_text.replace('</h-l-1>', '')
        highlighted_text = highlighted_text.replace('<h-l-2>', '')
        highlighted_text = highlighted_text.replace('</h-l-2>', '')
        highlighted_text = highlighted_text.replace('<h-l-3>', '')
        highlighted_text = highlighted_text.replace('</h-l-3>', '')
        highlighted_text = highlighted_text.replace('<h-l-4>', '')
        highlighted_text = highlighted_text.replace('</h-l-4>', '')
    }
    $('<div>'+highlighted_text+'</div>').appendTo(textDiv)
}

function load_target(Counter) {
    var textDiv = $('#background_screen' + taskCounter)
    var sample = sample_indices[taskCounter-1]
    fetch('static/examples/'+examples_dir+'/tgt_' + sample + '.txt')
        .then(response => response.text())
        .then(text => display_target(Counter, textDiv, text))
}

function fg_bg_screen(i, notes, num_tasks, language){
    var num = i;
    screen = create_screen(taskCounter, notes, num_tasks, language)
    $(screen).appendTo('#task_screen'+i)
    $('<p class="background_screen" id="background_screen'+taskCounter+'"></p>').appendTo('#bg_placeholder'+taskCounter)
}


function feedback_screen(i, notes){
    if(w_hl==false){
    $(
        '<div class="panel panel-primary">\
            <div class="panel-heading">\
                <div><strong>Feedback</strong> </div>\
            </div>\
            <div class="task">\
                <p>Please provide your feedback on the survey.</p>\
                <input type="text" class="form-control" name="feedback" id="feedback" rows="5" value=""></input> \
            </div>\
        </div>'
    ).appendTo('#task_screen'+i)}
    if(w_hl==true){
    $(
        '<div class="panel panel-primary">\
            <div class="panel-heading">\
                <div><strong>Feedback</strong> </div>\
            </div>\
            <div class="task">\
                <p>Please provide your feedback on the usefulness of highlights.</p>\
                <input type="text" class="form-control" name="feedback" id="feedback" rows="5" value=""></input> \
            </div>\
        </div>'
    ).appendTo('#task_screen'+i)}
}


function create_screen(i, notes, num_tasks, language){
    screen = '<div class="panel panel-info">\
            <div class="panel-heading">\
                <div style="float:left; width:80%"><strong>Task-'+i+'</strong> </div>\
                <div style="display: flex; align-items:center;">\
                    <span style="margin-right:10px">'+i+'/'+num_tasks+'</span><progress id="file" value="'+i+'" max="'+num_tasks+'"></progress>\
                </div>\
            </div>\
            <div class="task">\
                <div style="font-size:16px">\
                    </span>\
                </div>\
                <div class=row>\
                    <div class="col-md-12">\
                        <p class="text_screen" id="text_screen'+i+'"></p>\
                    </div>\
                    <div class="col-md-12">\
                        <div id="bg_placeholder'+i+'"></div>\
                    </div>\
                </div>\
                <div class="row">\
                    <div class="col-md-12">\
                        <div style="margin-top:20px;">\
                           <strong> Does the translated text contain an accuracy error? </strong>\
                        </div>\
                        <div  style="margin-left:40px; margin-top:10px;">\
                            <input type="radio" id="yes'+i+'" name="t'+i+'" value="yes">\
                            <label for="yes'+i+'" style="margin-right:10px; margin-left:5px; font-weight: normal;">Yes</label>\
                            <input type="radio" id="no'+i+'" name="t'+i+'" value="no">\
                            <label for="no'+i+'" style="margin-left:5px; font-weight: normal;">No</label>\
                       <br>\
                       </br>\
                        </div>\
                        <div class="col-md-5" >\
                        <div class="form-group">\
                            <label for="class'+i+'">Select the severity of the accuracy error.</label>\
                            <select class="form-control" name="class'+i+'">\
                              <option>N/A</option>\
                              <option>⚠️ Minor </option>\
                              <option>🛑 Major</option>\
                            </select>\
                        </div>\
                        </div>\
                </div>\
            </div>\
        </div>'

    return screen
}


function demographic_screen(i){
    $(
        '<div class="panel panel-primary">\
            <div class="panel-heading">\
                <div><strong>Demographic Information</strong> </div>\
            </div>\
            <div class="task">\
                <div style="margin-top:20px;">Gender Identity (select all that apply)</div>\
                <div  style="margin-left:40px; margin-top:10px;">\
                    <input type="checkbox" id="gender_w" name="gender" value="woman">\
                    <label for="gender_w" style="margin-right:10px; margin-left:5px; font-weight: normal;">Woman</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="checkbox" id="gender_m" name="gender" value="man">\
                    <label for="gender_m" style="margin-right:10px; margin-left:5px; font-weight: normal;">Man</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="checkbox" id="gender_t" name="gender" value="transgender">\
                    <label for=gender_t" style="margin-right:10px; margin-left:5px; font-weight: normal;">Transgender</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="checkbox" id="gender_nb" name="gender" value="nonbinary_nonconf">\
                    <label for="gender_nb" style="margin-right:10px; margin-left:5px; font-weight: normal;">Non-binary/non-conforming</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="checkbox" id="gender_d" name="gender" value="different">\
                    <label for="gender_d" style="margin-right:10px; margin-left:5px; font-weight: normal;">A different gender identity</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="checkbox" id="gender_nr" name="gender" value="noresponse">\
                    <label for="gender_nr" style="margin-right:10px; margin-left:5px; font-weight: normal;">Prefer not to respond</label>\
                </div>\
                <div style="margin-top:20px;">How would you rate your proficiency in <strong>English</strong>? [Note that any answer is not a disadvantage, so please try to answer this as accurately as possible.] </div>\
                <div  style="margin-left:40px; margin-top:10px;">\
                    <input type="radio" id="No_prof" name="language" value="No_prof">\
                    <label for="age_18to25" style="margin-right:10px; margin-left:5px; font-weight: normal;">No proficiency</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="radio" id="Elementary" name="language" value="Elementary">\
                    <label for="age_25to40" style="margin-right:10px; margin-left:5px; font-weight: normal;">Elementary proficiency</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="radio" id="Limited" name="language" value="Limited">\
                    <label for=age_40to60" style="margin-right:10px; margin-left:5px; font-weight: normal;">Limited working proficiency</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="radio" id="Professional" name="language" value="Professional">\
                    <label for="age_over60" style="margin-right:10px; margin-left:5px; font-weight: normal;">Professional working proficiency</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="radio" id="full" name="language" value="full">\
                    <label for="age_nr" style="margin-right:10px; margin-left:5px; font-weight: normal;">Full professional proficiency</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="radio" id="native" name="language" value="native">\
                    <label for="age_nr" style="margin-right:10px; margin-left:5px; font-weight: normal;">Native or bilingual proficiency</label>\
                </div>\
                   <div style="margin-top:20px;">How would you rate your proficiency in <strong>Portuguese</strong>? [Note that any answer is not a disadvantage, so please try to answer this as accurately as possible.] </div>\
                <div  style="margin-left:40px; margin-top:10px;">\
                    <input type="radio" id="No_prof" name="language_pt" value="No_prof">\
                    <label for="age_18to25" style="margin-right:10px; margin-left:5px; font-weight: normal;">No proficiency</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="radio" id="Elementary" name="language_pt" value="Elementary">\
                    <label for="age_25to40" style="margin-right:10px; margin-left:5px; font-weight: normal;">Elementary proficiency</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="radio" id="Limited" name="language_pt" value="Limited">\
                    <label for=age_40to60" style="margin-right:10px; margin-left:5px; font-weight: normal;">Limited working proficiency</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="radio" id="Professional" name="language_pt" value="Professional">\
                    <label for="age_over60" style="margin-right:10px; margin-left:5px; font-weight: normal;">Professional working proficiency</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="radio" id="full" name="language_pt" value="full">\
                    <label for="age_nr" style="margin-right:10px; margin-left:5px; font-weight: normal;">Full professional proficiency</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="radio" id="native" name="language_pt" value="native">\
                    <label for="age_nr" style="margin-right:10px; margin-left:5px; font-weight: normal;">Native or bilingual proficiency</label>\
                </div>\
                  <div style="margin-top:20px;">Age group</div>\
                <div  style="margin-left:40px; margin-top:10px;">\
                    <input type="radio" id="age_18to25" name="age" value="18to25">\
                    <label for="age_18to25" style="margin-right:10px; margin-left:5px; font-weight: normal;">18-25</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="radio" id="age_25to40" name="age" value="25to40">\
                    <label for="age_25to40" style="margin-right:10px; margin-left:5px; font-weight: normal;">25-40</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="radio" id="age_40to60" name="age" value="40to60">\
                    <label for=age_40to60" style="margin-right:10px; margin-left:5px; font-weight: normal;">40-60</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="radio" id="age_over60" name="age" value="over60">\
                    <label for="age_over60" style="margin-right:10px; margin-left:5px; font-weight: normal;">\>60</label>\
                </div>\
                <div  style="margin-left:40px;">\
                    <input type="radio" id="age_nr" name="age" value="noresponse">\
                    <label for="age_nr" style="margin-right:10px; margin-left:5px; font-weight: normal;">Prefer not to respond</label>\
                </div>\
            </div>\
        </div>'
    ).appendTo('#task_screen'+i)
    $('.error').hide();
}


function confidence_atncheck(i, notes, language){
    $(
        '<div class="panel panel-danger">\
            <div class="panel-heading">\
                <div>&#128218; <strong> <span style="color:#CA0B00"> Review </span></strong> </div>\
            </div>\
                <div style="margin:20px 5px 15px 20px;">\
                <div class="row">\
                     <div class="col-md-5" >\
                        <div class="form-group">\
                            <label for="atncheck1">What was your response to the previous request: Select the severity of the accuracy error.</label>\
                            <select class="form-control" name="atncheck1">\
                              <option>N/A</option>\
                              <option>⚠️ Minor</option>\
                              <option>🛑 Major</option>\
                            </select>\
            </div>\
            </div>\
            </div>\
        </div>'
    ).appendTo('#task_screen'+i)
}


function agreement_atncheck(i, notes){
    $(
        '<div class="panel panel-danger">\
            <div class="panel-heading">\
                <div>&#128218; <strong> <span style="color:#CA0B00"> Review </span></strong> </div>\
            </div>\
            <div class="task">\
                <div>What was your answer to the previous question: Does the translated text contain an accuracy error?</div>\
                <div  style="margin-left:40px; margin-top:10px;">\
                    <input type="radio" id="yes'+i+'" name="atncheck2" value="yes">\
                    <label for="yes'+i+'" style="margin-right:10px; margin-left:5px; font-weight: normal;">Yes</label>\
                    <input type="radio" id="no'+i+'" name="atncheck2" value="no">\
                    <label for="no'+i+'" style="margin-left:5px; font-weight: normal;">No</label>\
                </div>\
            </div>\
        </div>'
    ).appendTo('#task_screen'+i)
}

function create_response_screen(save_name){
    $(
        '<div>Your response has been saved. Thank you for taking the survey!<br/> \
        Your submission code for prolific is: <b>'+save_name+'</b></div>\
        <div>You may now close the tab.</div>'
    ).appendTo('#response_screen')
}