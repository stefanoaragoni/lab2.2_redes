import java.util.Scanner;

public class Hamming_Receptor {
    public static int detectError(String arr, int nr) {
        int n = arr.length();
        int res = 0;

        for (int i = 0; i < nr; i++) {
            int val = 0;
            for (int j = 1; j <= n; j++) {
                if ((j & (1 << i)) == (1 << i)) {
                    val = val ^ Character.getNumericValue(arr.charAt(n - j));
                }
            }
            res += val * (int) Math.pow(10, i);
        }

        return Integer.parseInt(String.valueOf(res), 2);
    }

    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            System.out.println("=========== Hamming Receptor ===========");
            System.out.print("Trama: ");
            String receivedData = scanner.nextLine();
            receivedData = receivedData.replaceAll("\\s", "");

            // Determine the positions of Redundant Bits
            int m = receivedData.length();
            int r = 0;
            for (int i = 0; i < m; i++) {
                if (Math.pow(2, i) >= m + i + 1) {
                    r = i;
                    break;
                }
            }

            int errorPosition = detectError(receivedData, r);

            if (errorPosition != 0 && errorPosition <= m) {
                StringBuilder correctedData = new StringBuilder(receivedData);
                int errorBit = m - errorPosition;
                char currentBit = receivedData.charAt(errorBit);
                correctedData.setCharAt(errorBit, (currentBit == '0') ? '1' : '0');
                receivedData = correctedData.toString();

                System.out.println("Errores Detectado en la posicion: " + errorBit + " (de derecha a izquieda comenzando por 0).");
            }

            if (errorPosition == 0) {
                System.out.println("No error detectado en la trama.");
                System.out.println("Trama " + receivedData);
            } else if (errorPosition > 0 && errorPosition <= m) {
                System.out.println("Error detectado y corregido en la trama.");
                System.out.println("Trama correcta " + receivedData);
            } else {
                System.out.println("Errores detectados en la trama.");
                System.out.println("Se descarta la trama por errrores no corregibles.");
            }
        }
    }
}
