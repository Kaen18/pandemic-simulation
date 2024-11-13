import { Request, Response, Router } from "express";
import { start } from "../controller/pandemia";

const router = Router();

router.post("/start", start);



export { router };