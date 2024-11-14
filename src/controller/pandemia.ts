import { Request, Response } from "express";
import { PandemiaService } from "../services";

export const start = async (req: Request, res: Response) => {
    const pandemiaService = new PandemiaService();
    const result = await pandemiaService.start(req.body);
    res.send(result);
}

export const pause = async (_: Request, res: Response) => {
    const pandemiaService = new PandemiaService();
    const result = pandemiaService.pause();
    res.send(result);
}