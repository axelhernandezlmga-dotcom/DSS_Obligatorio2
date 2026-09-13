package com.cinebuscador.config;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

/**
 * Servicio de hashing de contraseñas con BCrypt (una sola vía, con salt
 * aleatorio por contraseña).
 */
public class EncryptionService {

    private static final BCryptPasswordEncoder ENCODER = new BCryptPasswordEncoder();

    public static String hash(String plaintext) {
        return ENCODER.encode(plaintext);
    }

    public static boolean matches(String plaintext, String hash) {
        return ENCODER.matches(plaintext, hash);
    }
}
