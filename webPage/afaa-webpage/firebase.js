// firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// Delete contents for every push
const firebaseConfig = {
};

const app = initializeApp(firebaseConfig);

const auth = getAuth(app);
const db = getFirestore(app);

console.log(app);
console.log(auth);
console.log(db);

export { auth, db };
