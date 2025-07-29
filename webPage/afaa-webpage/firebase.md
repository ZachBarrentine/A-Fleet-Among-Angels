
````markdown
# Firebase Frontend App

This project uses Firebase Authentication and Firestore.

---

## 🔧 Setup

1. Install dependencies  
   ```bash
   npm install
````

2. Start the dev server

   ```bash
   npm run dev
   ```

3. Firebase is preconfigured in `firebase.js`. No need to modify unless switching projects.

---

## 🔐 Firebase Services Used

* **Authentication** (Email/Password)
* **Firestore Database**

Firestore access is restricted to authenticated users:

```js
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

---

## 🧪 Common Usage

### Import Firebase Services

```js
import { auth, db } from './firebase';
```

### Create user

```js
import { createUserWithEmailAndPassword } from 'firebase/auth';
createUserWithEmailAndPassword(auth, email, password);
```

### Sign in

```js
import { signInWithEmailAndPassword } from 'firebase/auth';
signInWithEmailAndPassword(auth, email, password);
```

### Add to Firestore

```js
import { collection, addDoc } from 'firebase/firestore';
addDoc(collection(db, 'users'), { name: 'Jane' });
```

---

## 📦 Build for Production

```bash
npm run build
```

Deploy the `dist` folder.

---


```
```
