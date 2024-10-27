import { Request, Response, Router } from "express";
import { start } from "../controller/pandemia";

const router = Router();

router.get("/start", start);

export { router };