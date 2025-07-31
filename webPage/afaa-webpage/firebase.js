// firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyDWNIMHbms4-eZmJU1TyzopglWv9XmQ5Dc",
  authDomain: "a-fleet-among-angels.firebaseapp.com",
  projectId: "a-fleet-among-angels",
  storageBucket: "a-fleet-among-angels.firebasestorage.app",
  messagingSenderId: "771188935939",
  appId: "1:771188935939:web:caeecf66172cb00be76d36"
};

const app = initializeApp(firebaseConfig);

const auth = getAuth(app);
const db = getFirestore(app);

console.log(app);
console.log(auth);
console.log(db);

export { auth, db };
