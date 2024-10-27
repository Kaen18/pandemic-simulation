import "dotenv/config";
import express from "express";
import cors from "cors";
import { router } from "./src/routes";
const PORT = process.env.PORT || 3000;
const app = express();
app.use(
  cors({
    origin: "*",
  })
);
app.use(express.json())
app.use(router);
app.listen(PORT, () => console.log(`Listen in port ${PORT}`));