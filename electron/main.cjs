const { app, BrowserWindow } = require("electron");
const axios = require("axios");

const { createTray } = require("./tray.cjs");

let mainWindow;

// Track whether the application is actually quitting
app.isQuiting = false;

async function waitForBackend() {
    console.log("⏳ Waiting for backend...");

    while (true) {
        try {
            await axios.get("http://127.0.0.1:5001/docs");
            console.log("✅ Backend Ready");
            return;
        } catch {
            await new Promise((resolve) => setTimeout(resolve, 1000));
        }
    }
}

async function waitForFrontend() {
    console.log("⏳ Waiting for frontend...");

    while (true) {
        try {
            await axios.get("http://localhost:3000");
            console.log("✅ Frontend Ready");
            return;
        } catch {
            await new Promise((resolve) => setTimeout(resolve, 1000));
        }
    }
}

async function createWindow() {
    try {
        console.log("1️⃣ Waiting for Backend...");
        await waitForBackend();

        console.log("2️⃣ Waiting for Frontend...");
        await waitForFrontend();

        console.log("3️⃣ Creating BrowserWindow...");

        mainWindow = new BrowserWindow({
            width: 1400,
            height: 900,

            minWidth: 1100,
            minHeight: 700,

            title: "AI IT Support Agent",

            autoHideMenuBar: true,

            webPreferences: {
                contextIsolation: true,
                nodeIntegration: false
            }
        });

        console.log("4️⃣ BrowserWindow Created");

        // Create the system tray
        createTray(mainWindow);

        // Hide window instead of closing
        mainWindow.on("close", (event) => {
            if (!app.isQuiting) {
                event.preventDefault();
                mainWindow.hide();
            }
        });

        mainWindow.on("closed", () => {
            console.log("🛑 Window Closed");
            mainWindow = null;
        });

        console.log("5️⃣ Loading URL...");

        await mainWindow.loadURL("http://localhost:3000");

        // Reduce UI scaling (adjust between 0.8 and 1.0 as needed)
        mainWindow.webContents.setZoomFactor(0.70);

        console.log("6️⃣ URL Loaded Successfully");

        mainWindow.show();

        console.log("7️⃣ Window Displayed");

    } catch (err) {
        console.error("❌ Electron Error:");
        console.error(err);
    }
}

app.whenReady().then(() => {
    console.log("🚀 Electron Ready");
    createWindow();
});

app.on("activate", () => {
    if (mainWindow) {
        mainWindow.show();
        mainWindow.focus();
    } else {
        createWindow();
    }
});

app.on("before-quit", () => {
    app.isQuiting = true;
});

app.on("window-all-closed", () => {
    // Keep the application alive while it's in the system tray.
});