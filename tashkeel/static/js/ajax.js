
function printDict(data){
    html = ''
    for(var type in data){
        html += '<span class="text-primary">'+type+'</span> : '+data[type]+'</br>'
    }
    return html
}
$(document).ready(function() {
    $("#gohome").click(function(){
        $("#home").show()
        $("#evaluate").hide()
        $("#activehome").addClass( "active" );
        $("#activeeval").removeClass( "active" )
    });
    $("#goevaluate").click(function(){
        $("#home").hide()
        $("#evaluate").show()
        $("#activeeval").addClass( "active" );
        $("#activehome").removeClass( "active" )
    });

    $("#DoTashkeel_v1").click(function(){
         $("#statics_panel").hide()
         $("#results_panel").hide()
          $("#loading1").show()
         $.ajax({
           type: "POST",
           url: "/tashkeel_v1/",
           dataType: "json",
           traditional: true,
           data: {
                    'csrfmiddlewaretoken':$.cookie('csrftoken'),
                    'text': $("#text").val(),
                    'ConstLaplace' : $("#ConstLaplace").val()
                  },
           success: function(data) {
               $("#loading1").hide()
              $("#results_panel").show()
              $("#results").html(data['result'])
              $("#time").html('('+data['time']+' secodes)')
               if($("#showStatics").is(':checked')) {
                   $("#type").html(data['type'])
                   $("#token").html(data['token'])
                   $("#statics_panel").show()
               } else $("#statics_panel").hide()
            }
        });
    });

    $("#DoTashkeel_v2").click(function(){
         $("#statics_panel").hide()
         $("#results_panel").hide()
         $("#loading1").show()
         $.ajax({
           type: "POST",
           url: "/tashkeel_v2/",
           dataType: "json",
           traditional: true,
           data: {
                    'csrfmiddlewaretoken':$.cookie('csrftoken'),
                    'text': $("#text").val(),
                    'ConstLaplace' : $("#ConstLaplace").val()
                  },
           success: function(data) {
               $("#loading1").hide()
              $("#results_panel").show()
              $("#results").html(data['result'])
              $("#time").html('('+data['time']+' secodes)')
               if($("#showStatics").is(':checked')) {
                   $("#type").html(data['type'])
                   $("#token").html(data['token'])
                   $("#statics_panel").show()
               } else $("#statics_panel").hide()
            }
        });
    });

    $("#GetTestSents").click(function(){
         $("#results_panel_2").hide()
        $("#loading2").show()
         $.ajax({
           type: "POST",
           url: "/gettestsents/",
           dataType: "json",
           traditional: true,
           data: {
                    'csrfmiddlewaretoken':$.cookie('csrftoken'),
                    'nbrTestSents': $("#nbrTestSents").val(),
                    'ConstLaplace' : $("#ConstLaplace").val()
                  },
           success: function(data) {
              $("#loading2").hide()
              $("#TashkeelAndEvaluate").show()
              $("#text_2").val(data['sents_whitout_diac'])
              $("#sents_diac_corpus_value").val(data['sents_diac'])
             }
        });
    });

    $("#Evaluate").click(function(){
        $("#statics_panel_2").hide()
        $("#results_panel_2").hide()
        $("#loading2").show()
         $.ajax({
           type: "POST",
           url: "/evaluate/",
           dataType: "json",
           traditional: true,
           data: {
                    'csrfmiddlewaretoken':$.cookie('csrftoken'),
                    'text': $("#text_2").val(),
                    'sents_diac_corpus_value': $("#sents_diac_corpus_value").val(),
                    'ConstLaplace' : $("#ConstLaplace").val()
                  },
           success: function(data) {
              $("#loading2").hide()
              $("#results_panel_2").show()
              $("#results_2").hide()
              $("#time_2").html('('+data['time']+' secodes)')
              $("#type_2").html(data['type'])
              $("#token_2").html(data['token'])

              $("#recall").html(data['recall']+" %")
              $("#precision").html(data['precision']+" %")
              $("#fmeasure").html(data['fmeasure']+" %")
              $("#statics_panel_2").show()
            }
        });
    });

    $("#TashkeelAndEvaluate").click(function(){
        //$("#accuracy_panel").hide()
        $("#statics_panel_2").hide()
        $("#results_panel_2").hide()
        $("#loading2").show()
         $.ajax({
           type: "POST",
           url: "/tashkeelandevaluate/",
           dataType: "json",
           traditional: true,
           data: {
                    'csrfmiddlewaretoken':$.cookie('csrftoken'),
                    'text': $("#text_2").val(),
                    'sents_diac_corpus_value': $("#sents_diac_corpus_value").val(),
                    'ConstLaplace' : $("#ConstLaplace").val()
                  },
           success: function(data) {
              $("#loading2").hide()
              $("#results_panel_2").show()
              $("#results_2").show()
              $("#results_2").html(data['result'])
              $("#time_2").html('('+data['time']+' secodes)')
              $("#type_2").html(data['type'])
              $("#token_2").html(data['token'])

              $("#wer1_recall").html(data['wer1_recall']+" %")
              $("#wer1_precision").html(data['wer1_precision']+" %")
              $("#wer1_fmeasure").html(data['wer1_fmeasure']+" %")
              

              $("#wer2_recall").html(data['wer2_recall']+" %")
              $("#wer2_precision").html(data['wer2_precision']+" %")
              $("#wer2_fmeasure").html(data['wer2_fmeasure']+" %")
              
              

              $("#der1_recall").html(data['der1_recall']+" %")
              $("#der1_precision").html(data['der1_precision']+" %")
              $("#der1_fmeasure").html(data['der1_fmeasure']+" %")
              
              

              $("#der2_recall").html(data['der2_recall']+" %")
              $("#der2_precision").html(data['der2_precision']+" %")
              $("#der2_fmeasure").html(data['der2_fmeasure']+" %")
              $("#statics_panel_2").show()
            }
        });
    });

    $("#GetDict").click(function(){
        //$("#accuracy_panel").hide()
        $("#statics_panel").hide()

        $("#results_panel").hide()
        $("#loading1").show()
         $.ajax({
           type: "POST",
           url: "/getdict/",
           dataType: "json",
           traditional: true,
           data: {
                    'csrfmiddlewaretoken':$.cookie('csrftoken'),
                    'text': $("#text").val()
                  },
           success: function(data) {
               $("#loading1").hide()
               $("#results_panel").show()
                $("#results").html(printDict(data['results']))
                $("#time").html('('+data['time']+' secodes)')
               if($("#showStatics").is(':checked')) {
                   $("#type").html(data['type'])
                   $("#token").html(data['token'])
                   $("#statics_panel").show()
               } else $("#statics_panel").hide()
            }
        });
    });


    $("#DeleteDiact").click(function(){
         $("#accuracy_panel").hide()
         $("#statics_panel").hide()

         $("#results_panel").hide()
         $("#loading1").show()
         $.ajax({
           type: "POST",
           url: "/deletediac/",
           dataType: "json",
           traditional: true,
           data: {
                    'csrfmiddlewaretoken':$.cookie('csrftoken'),
                    'text': $("#text").val()
                  },
           success: function(data) {
               $("#loading1").hide()
               $("#results_panel").show()
               $("#results").html(data['results'])
               $("#time").html('('+data['time']+' secodes)')
             }
        });
    });

    $('[data-toggle="tooltip"]').tooltip();
})
                   
            
