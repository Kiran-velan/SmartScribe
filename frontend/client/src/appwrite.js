import { Client, Account, Databases } from "appwrite";

const client = new Client()
    .setEndpoint(process.env.REACT_APP_APPWRITE_ENDPOINT)
    .setProject(process.env.REACT_APP_APPWRITE_PROJECT_ID);

console.log("Appwrite endpoint:", process.env.REACT_APP_APPWRITE_ENDPOINT);
console.log("Appwrite project ID:", process.env.REACT_APP_APPWRITE_PROJECT_ID);

const account = new Account(client);
const databases = new Databases(client);

export { client, account, databases };
