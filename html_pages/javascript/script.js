
const messagesContainer = document.querySelector(".messages-container");
const messageInput = document.getElementById("messageInput");
const sendMessageButton = document.getElementById("sendMessage");
const friendsList = document.getElementById("friendsList");
const askForUsersButton = document.getElementById("askForUsers");
const get_roomButton = document.getElementById("get_rooms");
let users = [];
let chat_id;

// Connect to WebSocket server
const ws = new WebSocket("ws://" + window.location.host + "/ws");

console.log("Connecting to server at " + window.location.href);

function appendToURL(key, value) {
  let url = new URL(window.location.href);
  url.searchParams.set(key, value); // Add or update query param
  window.history.pushState({}, "", url);
}

ws.onopen = () => {
  console.log("Connected to server");
  ws.send(JSON.stringify({ action: "get_users" })); // Request user list
};

ws.onclose = () => console.log("Disconnected from server");
ws.onerror = (error) => console.error("WebSocket error:", error);

ws.onmessage = (event) => {
  try {
    const received_data = JSON.parse(event.data);

    switch (received_data.action) {
      case "users_list":
        users = received_data.users;
        renderFriendsList();
        break;
      case "new_message":
        displayMessage(received_data.message, "friend");
        break;
      case "ping":
        setTimeout(() => ws.send(JSON.stringify({ action: "pong" })), 1000);
        break;
      case "chat_id":
        chat_id = received_data.chat_id;
        console.log("Chat ID:", chat_id);
        break;
      case "messages":
        console.log("Received messages:", received_data.messages);
        let usernameCookie = document.cookie
          .split("; ")
          .find((row) => row.startsWith("username="));
        let sender_username = usernameCookie
          ? usernameCookie.split("=")[1]
          : null;
        if (!sender_username) {
          console.error("Username not found in cookies.");
        }
        received_data.messages.forEach((message) => {
          if (message.sender_username === sender_username) {
            displayMessage(message.content, "own");
          } else {
            displayMessage(message.content, "friend");
          }
        });
        break;
      default:
        console.error("Unknown action:", received_data.action);
    }
  } catch (error) {
    console.error("Error parsing WebSocket message:", error);
  }
};

askForUsersButton.addEventListener("click", () => {
  ws.send(JSON.stringify({ action: "get_users" })); // Request user list
});

get_roomButton.addEventListener("click", () => {
  ws.send(JSON.stringify({ action: "get_rooms" })); // Request user list
});

// Function to render friends list dynamically
function renderFriendsList() {
  friendsList.innerHTML = ""; // Clear existing friends list
  users.forEach((user) => {
    const friend = document.createElement("li");
    friend.classList.add(
      "friend",
      "p-3",
      "bg-gray-300",
      "rounded-lg",
      "mb-2",
      "cursor-pointer",
      "hover:bg-white"
    );
    friend.textContent = user.display_name;
    friend.setAttribute("data-name", user.display_name);
    friendsList.appendChild(friend);
  });
}

// Event delegation for friend selection
friendsList.addEventListener("click", (event) => {
  // ask server to create a chat and send the chat id
  // get the user id from cookies
  let usernameCookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith("username="));
  let sender_username = usernameCookie ? usernameCookie.split("=")[1] : null;
  if (!sender_username) {
    console.error("Username not found in cookies.");
  }

  let chat_with = document.getElementById("chatWith");
  chat_with.textContent = event.target.getAttribute("data-name");

//   appendToURL("username", event.target.getAttribute("data-name"));

  const messageData = {
    action: "get_chat_id",
    receiver_id: users.find(
      (user) => user.display_name === event.target.getAttribute("data-name")
    ).user_id,
    sender_username: sender_username,
  };
  console.log(messageData);
  ws.send(JSON.stringify(messageData));

  if (typeof chat_id !== "undefined") {
    if (event.target.closest(".friend")) {
      document
        .querySelectorAll(".friend")
        .forEach((f) => f.classList.remove("bg-white"));
      event.target.classList.add("bg-white");

      const friendName = event.target.getAttribute("data-name");
      console.log("Selected friend:", friendName);
      console.log("Chat ID:", chat_id);

      messagesContainer.innerHTML = ""; // Clear messages when switching chat

      const messageData = {
        action: "get_messages",
        chat_id: chat_id,
      };
      ws.send(JSON.stringify(messageData));

      // messages.forEach((message) => {
      //     displayMessage(message.text, message.type);
      // });
    } else if (!event.target.closest(".friend")) {
      console.log("Clicked element is not a friend.");
      return;
    }
  } else {
    console.log("No chat selected.");
  }
});

messageInput.addEventListener("keypress", (event) => {
  if (event.key === "Enter") {
    sendMessageButton.click();
  }
});

// Send message
sendMessageButton.addEventListener("click", () => {
  const messageText = messageInput.value.trim();
  console.log("Sending message:", messageText);
  if (!messageText) return;

  let sender_username = document.cookie
    .split("; ")
    .find((row) => row.startsWith("username="))
    .split("=")[1];

  if (!chat_id) {
    console.error("No chat ID available. Cannot send message.");
    return;
  }

  const messageData = {
    action: "send_message",
    chat_id: chat_id, // Replace with actual selected friend
    message: messageText,
    sender_username: sender_username,
  };
  console.log("Message data:", messageData);
  ws.send(JSON.stringify(messageData));
  displayMessage(messageText, "own");
  messageInput.value = "";
});

// Function to display messages
function displayMessage(text, type) {
  const messageElement = document.createElement("div");
  messageElement.classList.add(
    "p-3",
    "rounded-lg",
    "w-fit",
    "max-w-xs",
    "mb-2"
  );

  if (type === "own") {
    messageElement.classList.add("bg-indigo-500", "text-white", "ml-auto");
  } else {
    messageElement.classList.add("bg-gray-300", "text-gray-800", "mr-auto");
  }

  messageElement.textContent = text;
  messagesContainer.appendChild(messageElement);
  messagesContainer.scrollTop = messagesContainer.scrollHeight; // Auto-scroll
}
