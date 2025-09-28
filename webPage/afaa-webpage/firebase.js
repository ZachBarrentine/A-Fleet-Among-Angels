// firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// Delete contents for every push
const firebaseConfig = {
    apiKey: "AIzaSyCzE4wbXqyNVyfZ3RWWOJSVatjXLEz2pQ8",
    authDomain: "a-fleet-among-angels.firebaseapp.com",
    projectId: "a-fleet-among-angels",
    storageBucket: "a-fleet-among-angels.firebasestorage.app",
    messagingSenderId: "771188935939",
    appId: "1:771188935939:web:0d5c97e0c365acbae76d36"
};

const app = initializeApp(firebaseConfig);

const auth = getAuth(app);
const db = getFirestore(app);

console.log(app);
console.log(auth);
console.log(db);

export { auth, db };
