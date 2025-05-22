function ensure_consent(element){
    if ($('input[name='+element+']:checked').length == 0) {
        $('.error').show();
        return 'fail';
    }
    return 'success';
}

// function init_toggle(){
//     // Instructions expand/collapse
//     var content = $('#instructionBody');
//     var trigger = $('#collapseTrigger');

//     return content, trigger
// }

// function toggle(trigger, content){
//     $('.collapse-text').text('(Click to collapse)');
//     trigger.click(function(){
//       content.toggle();
//       var isVisible = content.is(':visible');
//       if(isVisible){
//         $('.collapse-text').text('(Click to collapse)');
//       }else{
//         $('.collapse-text').text('(Click to expand)');
//       }
//     });

//     return content
// }

function init_toggle(){
    var content = $('#abbreviated-instructions .panel-body');
    var trigger = $('#collapseTriggerInstructions');

    toggle(trigger, content);
}

function toggle(trigger, content){
    trigger.click(function(){
        let isCurrentlyVisible = content.is(':visible');

        // Toggle content
        content.slideToggle(200);

        // Update arrow immediately based on *current* state
        // If currently visible, we're about to hide → show ▼
        // If currently hidden, we're about to show → show ▲
        trigger.find('.collapse-icon').text(isCurrentlyVisible ? '▼' : '▲');
    });
}

function updateNotes(Counter, notes){
    if (document.getElementById("notes"+Counter)){
        notes = document.getElementById("notes"+Counter).value;
        return notes
    } else {
        return
    }
}

function showAtnCheckScreen(Counter){
    if (Counter==atncheck1){
        confidence_atncheck(Counter)
    } else{
        agreement_atncheck(Counter)
    }
    var screen = '#screen' + Counter;
    $(screen).show();
    return 
}

function hideCurrScreen(Counter, notes){
    var screen = '#screen' + Counter;
    $(screen).hide();
}

function showNewScreen(Counter, notes, language){

    Counter +=1;

    if(Counter==atncheck1 || Counter==atncheck2){
        showAtnCheckScreen(Counter)
        return Counter;
    }

    taskCounter += 1

    if(taskCounter==num_tasks+1){
        agg_screen(Counter, notes);
        var screen = '#screen' + Counter;
        $(screen).show();
        return Counter
    }

    if(taskCounter==num_tasks+2){
        feedback_screen(Counter, notes);
        var screen = '#screen' + Counter;
        $(screen).show();
        return Counter
    }

    if(taskCounter==num_tasks+3){
        demographic_screen(Counter);
        var screen = '#screen' + Counter;
        $(screen).show();
        return Counter
    }

    fg_bg_screen(Counter, notes, num_tasks, language);
    load_target(Counter)


    load_source(Counter).then((value) => {
        manage_highlights()
        .then((value)=>{
            var screen = '#screen' + Counter;
            $(screen).show();
        })
    });
    return Counter
}


function collateResults(results){
    results.push({name: "sample_indices", value: sample_indices});
    results.push({name: "with_hl", value: w_hl});
    results.push({name: "startTime", value: startTime});
    results.push({name: "surveyStartTime", value: surveyStartTime});
    results.push({name: "endTime", value: endTime});
    var timeInMinutes = (endTime-startTime)/60000;
    results.push({name: "totalTimeInMinutes", value: timeInMinutes});
    var timeInMinutes = (endTime-surveyStartTime)/60000;
    results.push({name: "surveyTimeInMinutes", value: timeInMinutes});

    return results
}

const manage_highlights = () => {
    if(w_hl==false){ 
        elems = document.getElementsByTagName('h-l')
        for (var i = 0; i < elems.length; i++) {
            elems[i].style.backgroundColor = "transparent";
        }
    }
    return Promise.resolve('success')
}

const removeBackground = () => {
    return Promise.resolve('success')
}