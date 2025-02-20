-- CreateTable
CREATE TABLE "News" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "date" DATETIME NOT NULL,
    "platform" TEXT NOT NULL,
    "author" TEXT NOT NULL,
    "ticker" TEXT NOT NULL,
    "sentiment" REAL NOT NULL
);
