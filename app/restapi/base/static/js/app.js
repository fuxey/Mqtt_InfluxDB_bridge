const subscribeBtn = document.querySelector('#subscribe-btn');
const subscribeTopic = document.querySelector('#topic');
const subscribeMeasurementName = document.querySelector('#measurementName');
const subscribeHostName = document.querySelector('#hostName');
const subscribeDataBaseName = document.querySelector('#dbName');



const snackbarContainer = document.querySelector('#confirmation-toast');
const showTopicsbtn = document.querySelector('#showtopics-btn');
const topicList = document.querySelector('#topic-list');

const unsubscribeBtn = document.querySelector('#unsubscribe-btn');
const unsubscribeInput = document.querySelector('#untopic');
const unsubscribeLabel = document.querySelector('#untopic-lbl');

const createDatabaseBtn = document.querySelector('#createdatabase-btn');
const createDataBaseInput = document.querySelector('#createdatabase');




createDatabaseBtn.addEvenetListener('click', (evt) => {
    const postData = {"databaseName": createDataBaseInput.value};
    fetch('/create_database', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData),
    }).then(value => {
        console.log("data send successfully");
        const data = {message: 'create database, successful'};
        snackbarContainer.MaterialSnackbar.showSnackbar(data);
        createDataBaseInput.value = "";
    }).catch(reason => {
        const data = {message: 'create Database no successful'};
        snackbarContainer.MaterialSnackbar.showSnackbar(data);
    });


});




setTimeout(a => {

    var data = {message: 'loading complete!'};
    snackbarContainer.MaterialSnackbar.showSnackbar(data);
}, 500);

unsubscribeBtn.addEventListener('click', (evt) => {
    const postData = {"topic": unsubscribeInput.value};
    fetch('/removeTopic', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData),
    }).then(value => {
        console.log("data sent successfully");
        const data = {message: 'subscribe to topic, successful!'};
        snackbarContainer.MaterialSnackbar.showSnackbar(data);
        if (document.getElementById(unsubscribeInput.value)) {
            document.getElementById(unsubscribeInput.value).remove();
        }
        unsubscribeInput.value = "";
    }).catch(reason => {
        const data = {message: 'subscribe to topic not successfully'};
        snackbarContainer.MaterialSnackbar.showSnackbar(data);
    });
});



subscribeBtn.addEventListener('click', (_event) => {
    console.log("button subscribe pressed!, push data", subscribeInput.value);
    const postData = { "topic": subscribeInput.value,
        "measurementName": subscribeMeasurementName.value,
        "hostName": subscribeHostName.value,
        "dbName": subscribeDataBaseName.value
    };
    fetch('/addSubscription', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData),
    }).then(value => {
        console.log("data sent successfully");
        const data = {message: 'subscribe to topic, successful!'};
        snackbarContainer.MaterialSnackbar.showSnackbar(data);
        subscribeInput.value="";
    }).catch(reason => {
        const data = {message: 'subscribe to topic not successfuly'};
        snackbarContainer.MaterialSnackbar.showSnackbar(data);
    });


});

const updateList = () => {

    fetch("/state", {}).then(value => {
        return value.json();
    }).then(value => {
        console.log(value);
        value.topics.map(value1 => {
            const entry = document.createElement('li');
            if (!document.getElementById(value1)) {
                entry.classList.add("mdl-list__item", "mdl-list__item-primary-content");
                entry.appendChild(document.createTextNode(value1));
                entry.setAttribute("id", value1);
                entry.addEventListener('click',ev => {
                   unsubscribeInput.value = value1;
                   unsubscribeLabel.remove();
                });
                topicList.appendChild(entry);
            }
        });
    });
};

setInterval((e) => {
    updateList();
}, 1000);


showTopicsbtn.addEventListener('click', evt => {
    updateList();
});

