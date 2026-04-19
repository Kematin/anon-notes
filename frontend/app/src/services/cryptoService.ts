export class CryptoService {
  private static readonly ITERATIONS = 100_000;

  private async deriveKey(password: string, salt: Uint8Array<ArrayBuffer>): Promise<CryptoKey> {
    const encoded = new TextEncoder().encode(password);

    const baseKey = await crypto.subtle.importKey("raw", encoded, "PBKDF2", false, ["deriveKey"]);

    return crypto.subtle.deriveKey(
      { name: "PBKDF2", salt, iterations: CryptoService.ITERATIONS, hash: "SHA-256" },
      baseKey,
      { name: "AES-GCM", length: 256 },
      false,
      ["encrypt", "decrypt"],
    );
  }

  async decryptNote(encyptedNote: string, password: string): Promise<string> {
    const bytes = Uint8Array.from(atob(encyptedNote), (c) => c.charCodeAt(0));

    const salt = bytes.slice(0, 16);
    const iv = bytes.slice(16, 28);
    const data = bytes.slice(28);

    const key = await this.deriveKey(password, salt);

    const decrypted = await crypto.subtle.decrypt({ name: "AES-GCM", iv }, key, data);

    return new TextDecoder().decode(decrypted);
  }

  async encryptNote(content: string, password: string): Promise<string> {
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const key = await this.deriveKey(password, salt);

    const encrypted = await crypto.subtle.encrypt(
      { name: "AES-GCM", iv },
      key,
      new TextEncoder().encode(content),
    );

    const result = new Uint8Array(salt.byteLength + iv.byteLength + encrypted.byteLength);
    result.set(salt, 0);
    result.set(iv, 16);
    result.set(new Uint8Array(encrypted), 28);

    return btoa(String.fromCharCode(...result));
  }
}

export const buildCryptoService = (): CryptoService => {
  const cryptoService = new CryptoService();
  return cryptoService;
};
