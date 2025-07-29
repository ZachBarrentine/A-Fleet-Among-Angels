// firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyCbWiK7q8Nh1-nYYPROPrgNZ8L1g5wIY5E",
  authDomain: "angels-6c2db.firebaseapp.com",
  projectId: "angels-6c2db",
  storageBucket: "angels-6c2db.firebasestorage.app",
  messagingSenderId: "312781630689",
  appId: "1:312781630689:web:853169fbbe625853731ba0",
  measurementId: "G-V1C9MTTM2T"
};

const app = initializeApp(firebaseConfig);

const auth = getAuth(app);
const db = getFirestore(app);

export { auth, db };
