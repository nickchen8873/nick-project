let port = process.env.VCAP_APP_PORT || 4000;
let axios1 = require("axios")
let axios2 = require("axios")
// let request = require("request");
let cheerio = require("cheerio")
// const fs = require('fs');
let express = require('express'),
    app = express();
let a = '', b = '';
let path = require('path');
let bodyparser = require('body-parser');
var comments = [];
var transComm = [];
var analComm = [];
let joygrade = 0;
let ConfidentGrade = 0;
let sadGrade = 0;
let fearGrade = 0;
let angerGrade = 0;
// var start = 0;
// var end = 0;

app.use(bodyparser.urlencoded({ extended: false }));

app.get('/', function (req, res) {
    res.sendFile(path.join(__dirname, 'views/index.html'));
})

app.post('/author', function (req, res) {
    // console.log(res)
    a = req.body.a;
    paspider(a)

    setTimeout(() => {
            res.send("平均每個人'高興'的程度百分比為 = " + (Math.round((joygrade / analComm.length* 100))/100) * 100  + "%" + 
            "   平均每個人'自信'的程度百分比為 = " + (Math.round((ConfidentGrade / analComm.length* 100))/100) * 100  + "%" +
            "   平均每個人'傷心'的程度百分比為 = " + (Math.round((sadGrade / analComm.length* 100))/100) * 100  + "%" +
            "   平均每個人'恐懼'的程度百分比為 = " + (Math.round((fearGrade / analComm.length* 100))/100) * 100  + "%" +
            "   平均每個人'生氣'的程度百分比為 = " + (Math.round((angerGrade / analComm.length* 100))/100) * 100  + "%" )
    }, 24000);
});

app.listen(port, function (req, res) {
    console.log(`Server started on port` + port);
});


function get() {
    
    const ToneAnalyzerV3 = require('ibm-watson/tone-analyzer/v3');
    const { IamAuthenticator } = require('ibm-watson/auth');

    const toneAnalyzer = new ToneAnalyzerV3({
        version: '2019-03-27',
        authenticator: new IamAuthenticator({
            apikey: 'IFU5iXLCde1fXT_a-RntOsFjn7hIHloPlN0rbn01etvQ',
        }),
        url: 'https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/22568da7-e1a2-4112-92fe-eeaed0eb0bda'
    });
    for(var i = 0; i < transComm.length; i++){
        const toneParams = {
            toneInput: { 'text': transComm[i]},
            contentType: 'application/json',
        };

        toneAnalyzer.tone(toneParams)
            .then(toneAnalysis => {
                analComm.push(JSON.parse(JSON.stringify(toneAnalysis, null, 2)));
                console.log("這是語意分析的結果:    "+JSON.stringify(toneAnalysis, null, 2));
            })
            .catch(err => {
                console.log('error:', err);
            });
    }
    setTimeout(() => {
        console.log("analComm.length = "+analComm.length)
        getjoy();
        getConfident();
        getSad();
        getFear();
        getAnger();
    }, 10000);
}


function temptranslate() {
    const LanguageTranslatorV3 = require('ibm-watson/language-translator/v3');
    const { IamAuthenticator } = require('ibm-watson/auth');
    const languageTranslator = new LanguageTranslatorV3({
        version: '2018-05-01',
        authenticator: new IamAuthenticator({
            apikey: 'RveXDgfU-1jWD8s3gf7q6fww4nnA0YZcot5-vcO8NWc5',
        }),
        url: 'https://api.us-south.language-translator.watson.cloud.ibm.com/instances/2abeae0d-d3c1-4235-a0aa-c05c527f4e4e',
    });
    for(var i = 0; i < comments.length; i++){
        const translateParams = {
            text: comments[i],
            modelId: 'zh-TW-en',
        };

        languageTranslator.translate(translateParams)
            .then(translationResult => {
                jsson = JSON.stringify(translationResult, null, 2);
                ttemp = JSON.parse(jsson);
                a = toString(ttemp.result.translations);
                transComm.push(ttemp.result.translations[0].translation.trim());
                console.log("這是翻譯的結果     :" + ttemp.result.translations[0].translation.trim());
            })
            .catch(err => {
                console.log('error:', err);
            });
    }
    setTimeout(() => {
        console.log("transComm.length = "+transComm.length)
        get();
    }, 5000);
}


function paspider(add) {
    uri = add.split("&");
    axios1.get(uri[0] + "&" + uri[1] + "&" + uri[2] ).then(res => {
        var $1 = cheerio.load(res.data);
        var temp1 = $1(".info-tab-list .sell-rating-list a div");
        var commStr;
        commStr = temp1.find("em").text().trim().substring(1);
        commNum = parseInt(commStr.split(")")[0]);
        pageNum = Math.ceil(commNum / 10);
        // 以下有設定最多只爬25頁，因為如果丟太多資料進去watson的服務分析的話，會被watson系統拒絕
        if (pageNum > 25){
            pageNum = 25;
        }
        console.log(pageNum);
        for (var x = 1; x <= pageNum; x++) {
            axios2.get(uri[0] + "&" + uri[1] + "&" + uri[2] + x).then(resp => {
                var $2 = cheerio.load(resp.data);
                var lis = $2(".detail-info tbody tr");
                for (var i = 0; i < lis.length;i++) {
                    var li = lis.eq(i);
                    if ( li.find(".Opinion p").text().split(2)[0].trim() != '此為系統預設給的正面評價' ){
                        comments.push(li.find(".Opinion p").text().split(2)[0].trim());
                    }
                }
                    console.log(comments);
            });
        }
    });
    setTimeout(() => {
        for (var y = 0; y < comments.length;y++) {
            console.log("這是爬蟲的結果     :" + comments[y])
        }
        console.log("comments.length = "+comments.length)
        temptranslate()
    }, 7000);
}


function getjoy(num) {
    for(i = 0;i<analComm.length;i++){
        aarry = analComm[i].result.document_tone.tones
        console.log(aarry)

        for(y = 0;y<aarry.length;y++){
            if(aarry[y].tone_name == 'Joy'){
                console.log(aarry[y].score +typeof(aarry[y].score))
                joygrade+=aarry[y].score
                console.log('jg = '+joygrade)
            }
        }
    }

    console.log('joy score is '+joygrade);
}


function getConfident(num) {
    for(i = 0;i<analComm.length;i++){
        aarry = analComm[i].result.document_tone.tones
        console.log(aarry)

        for(y = 0;y<aarry.length;y++){
            if(aarry[y].tone_name == 'Confident'){
                console.log(aarry[y].score +typeof(aarry[y].score))
                ConfidentGrade+=aarry[y].score
                console.log('conf = '+ConfidentGrade)
            }
        }
    }

    console.log('confient score is '+ConfidentGrade);
}


function getSad(num) {
    for(i = 0;i<analComm.length;i++){
        aarry = analComm[i].result.document_tone.tones
        console.log(aarry)

        for(y = 0;y<aarry.length;y++){
            if(aarry[y].tone_name == 'Sadness'){
                console.log(aarry[y].score +typeof(aarry[y].score))
                sadGrade+=aarry[y].score
                console.log('sad = '+sadGrade)
            }
        }
    }

    console.log('sadness score is '+sadGrade);
}


function getFear(num) {
    for(i = 0;i<analComm.length;i++){
        aarry = analComm[i].result.document_tone.tones
        console.log(aarry)

        for(y = 0;y<aarry.length;y++){
            if(aarry[y].tone_name == 'Fear'){
                console.log(aarry[y].score +typeof(aarry[y].score))
                fearGrade+=aarry[y].score
                console.log('fe = '+fearGrade)
            }
        }
    }

    console.log('fear score is '+fearGrade);
}


function getAnger(num) {
    for(i = 0;i<analComm.length;i++){
        aarry = analComm[i].result.document_tone.tones
        console.log(aarry)

        for(y = 0;y<aarry.length;y++){
            if(aarry[y].tone_name == 'Anger'){
                console.log(aarry[y].score +typeof(aarry[y].score))
                angerGrade+=aarry[y].score
                console.log('an = '+angerGrade)
            }
        }
    }

    console.log('anger score is '+angerGrade);
}

// visualRecong()

function visualRecong(){
    const VisualRecognitionV3 = require('ibm-watson/visual-recognition/v3');
    const { IamAuthenticator } = require('ibm-watson/auth');

    const visualRecognition = new VisualRecognitionV3({
    version: '2018-03-19',
    authenticator: new IamAuthenticator({
        apikey: 'Q3zWjKQF9dSm5UJJaPFO2aEFnIfFrS1zhILkZHjxPEog',
    }),
    url: 'https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/9b88603e-3bb6-4d92-a4af-ae8e078266c6',
    });

    const classifyParams = {
    imagesFile: fs.createReadStream('./emotionBackg.jpg'),
    owners: ['me'],
    threshold: 0.6,
    };

    visualRecognition.classify(classifyParams)
    .then(response => {
        const classifiedImages = response.result;
        console.log(JSON.stringify(classifiedImages, null, 2));
    })
    .catch(err => {
        console.log('error:', err);
    });
}