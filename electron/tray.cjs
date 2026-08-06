const { Tray, Menu, app } = require("electron");
const path = require("path");

let tray = null;

function createTray(mainWindow) {

    if (tray) {
        return tray;
    }

    tray = new Tray(
        path.join(__dirname, "assets", "AI_Assistant.png")
    );

    tray.setToolTip("AI IT Support Agent");

    const contextMenu = Menu.buildFromTemplate([
        {
            label: "Open",
            click: () => {
                if (mainWindow) {
                    mainWindow.show();
                    mainWindow.focus();
                }
            }
        },
        {
            type: "separator"
        },
        {
            label: "Exit",
            click: () => {
                app.isQuiting = true;

                if (mainWindow) {
                    mainWindow.destroy();
                }

                app.quit();
            }
        }
    ]);

    tray.setContextMenu(contextMenu);

    tray.on("double-click", () => {
        if (mainWindow) {
            mainWindow.show();
            mainWindow.focus();
        }
    });

    return tray;
}

module.exports = {
    createTray
};