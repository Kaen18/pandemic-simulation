import { Request, Response } from "express";
import { PandemiaService } from "../services";

export const start = async (req: Request, res: Response) => {
    const pandemiaService = new PandemiaService();
    const result = await pandemiaService.start();
    res.send(result);
}