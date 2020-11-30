const subscribeBtn = document.querySelector('#subscribe-btn');
const subscribeInput = document.querySelector('#topic')
const snackbarContainer = document.querySelector('#confirmation-toast');
const showTopicsbtn = document.querySelector('#showtopics-btn');
const topicList = document.querySelector('#topic-list');





setTimeout(a => {

    var data = {message: 'loading complete!'};
    snackbarContainer.MaterialSnackbar.showSnackbar(data);
},500);

subscribeBtn.addEventListener('click', (_event ) => {
    console.log("button subscribe pressed!, push data", subscribeInput.value);
    const postData = {"topic": subscribeInput.value };
    fetch('/addSubscription', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData),
    }).then (value => {
       console.log("data sent successfully");
       const data = {message: 'subscribe to topic, successful!'};
        snackbarContainer.MaterialSnackbar.showSnackbar(data);
    }).catch(reason => {
        const data = {message: 'subscribe to topic not successfuly'};
        snackbarContainer.MaterialSnackbar.showSnackbar(data);
    });


});

const updateList = () => {

   fetch("/state", {

   }).then(value => {
       return value.json();
   }).then(value => {
      console.log(value);
      value.topics.map(value1 => {
        const entry = document.createElement('li');
        if(!document.getElementById(value1)) {
            entry.classList.add("mdl-list__item", "mdl-list__item-primary-content");
            entry.appendChild(document.createTextNode(value1));
            entry.setAttribute("id",value1);
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

