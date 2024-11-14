import { Request, Response, Router } from "express";
import { pause, start } from "../controller/pandemia";

const router = Router();

router.post("/start", start);
router.get("/pause",  pause)



export { router };