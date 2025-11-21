import jwt from 'jsonwebtoken';
import { config } from '../config/env';

interface TokenPayload {
  userId: string;
  email: string;
}

export const createToken = (payload: TokenPayload) => {
  return jwt.sign(payload, config.jwtSecret, { expiresIn: '12h' });
};

export const verifyToken = (token: string): TokenPayload => {
  return jwt.verify(token, config.jwtSecret) as TokenPayload;
};
