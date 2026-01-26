const express = require("express");
const jwt = require("jsonwebtoken");
const fs = require("fs");
const helmet = require("helmet");

const app = express();
app.use(express.json());
app.use(helmet());

// SET PRIVATE KEY PATH VIA ENV
const PRIVATE_KEY_PATH = process.env.BB_ISS_PRIVATE_KEY;
if (!PRIVATE_KEY_PATH) {
  throw new Error("BB_ISS_PRIVATE_KEY env variable not set");
}

const privateKey = fs.readFileSync(PRIVATE_KEY_PATH);

app.post("/iss/token", (req, res) => {
  const { deviceId } = req.body;
  if (!deviceId) return res.status(400).json({ error: "deviceId required" });

  const token = jwt.sign(
    {
      deviceId,
      scope: "ISS_ACCESS",
      iss: "blackberry-iss"
    },
    privateKey,
    { algorithm: "RS256", expiresIn: "5m" }
  );

  res.json({ token });
});

app.listen(9443, () => console.log("BlackBerryISS running on 9443"));
