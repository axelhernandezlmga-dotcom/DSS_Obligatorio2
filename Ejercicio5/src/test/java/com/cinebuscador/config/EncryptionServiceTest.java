package com.cinebuscador.config;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class EncryptionServiceTest {

    // $2a$, costo de dos dígitos y 53 caracteres de salt + hash.
    private static final String FORMATO_BCRYPT =
        "^\\$2[aby]\\$\\d{2}\\$[./A-Za-z0-9]{53}$";

    @Test
    void verificaClaveCorrectaEIncorrecta() {
        String guardado = EncryptionService.hash("cine-seguro-2026");

        assertTrue(EncryptionService.matches("cine-seguro-2026", guardado));
        assertFalse(EncryptionService.matches("otra-clave", guardado));
        assertFalse(guardado.contains("cine-seguro-2026"));
    }

    @Test
    void mismaClaveGuardaValoresDistintos() {
        // Con AES/ECB y clave fija, dos usuarios con la misma clave quedan iguales.
        String primero = EncryptionService.hash("misma-clave");
        String segundo = EncryptionService.hash("misma-clave");

        assertNotEquals(primero, segundo);
        assertTrue(EncryptionService.matches("misma-clave", primero));
        assertTrue(EncryptionService.matches("misma-clave", segundo));
    }

    @Test
    void guardaUnHashBCryptConCostoMinimo() {
        String guardado = EncryptionService.hash("cine-seguro-2026");

        assertTrue(guardado.matches(FORMATO_BCRYPT));
        int costo = Integer.parseInt(guardado.substring(4, 6));
        assertTrue(costo >= 10, "Costo BCrypt demasiado bajo: " + costo);
    }
}
