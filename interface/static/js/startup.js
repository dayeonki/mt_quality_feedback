function main(){


    globalThis.startTime = Date.now()

    globalThis.atncheck1 = 3
    globalThis.atncheck2 = 9

    // sample_indices.splice(atncheck1, 0, -1)
    // sample_indices.splice(atncheck2, 0, -1)

    globalThis.num_tasks = 25;
    globalThis.taskCounter = 0
    globalThis.language = 'Portuguese'
    if(language == 'Spanish'){
        //globalThis.examples_dir = 'for_user_study/flores_gpt_es'
        globalThis.examples_dir = 'for_user_study/flores_gpt_paraphrase_es'
    }
    if(language == 'French'){
        //globalThis.examples_dir = 'for_user_study/flores_gpt_fr'
        globalThis.examples_dir = 'for_user_study/flores_gpt_paraphrase_fr'
    }
    if(language == 'Portuguese'){
        //globalThis.examples_dir = 'for_user_study/flores_gpt_el'
        globalThis.examples_dir = 'for_user_study/gpt_lit_en_pt_ced_0'
    }

    add_instructions('#instructions-text', language)
    manage_highlights()
    

    $('#instructions').hide();
    $('.error').hide();
    $('#answer-box').remove();

    // hide all screens initially
    var screen = $('.screen');
    screen.hide();

    function startTutorial(){

        $('#starttutorial_scrn').hide()

        if(language == 'French'){
          $('#spanish_tutorial').remove()
        }

        if(language == 'Spanish'){
          $('#french_tutorial').remove()
        }

        if(w_hl){
            $('#highlighted_text_wotutorial_s').hide()
        } else{
            $('#highlighted_text_tutorial_s').remove()
        }

        if(w_hl){
            $('#highlighted_text_wotutorial_t').hide()
        } else{
            $('#highlighted_text_tutorial_t').remove()
        }

        $('#tutorial').show()
        $('#startsurvey_scrn').show()
        introJs().start();
    }

    $('#starttutorial').click(function(){
        status_consent = ensure_consent('consent');
        if (status_consent=='success'){
            $('#consent').hide()
            add_instructions('#instructions-text-top', language)
            $('#instructions').show();
            startTutorial()
        }
    });

    $('#restart_tutorial').click(function(){
        introJs().start();
    })
}

