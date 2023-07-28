import java.util.Scanner;

public class Hamming_Receptor {
    public static int detectError(String arr, int nr) {
        int n = arr.length();
        int res = 0;

        // Calculate parity bits again
        for (int i = 0; i < nr; i++) {
            int val = 0;
            for (int j = 1; j <= n; j++) {
                if ((j & (1 << i)) == (1 << i)) {
                    val = val ^ Character.getNumericValue(arr.charAt(n - j));
                }
            }
            res += val * (int) Math.pow(10, i);
        }

        // Convert binary to decimal
        return Integer.parseInt(String.valueOf(res), 2);
    }

    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            System.out.print("Enter the received data: ");
            String receivedData = scanner.nextLine();

            // Determine the positions of Redundant Bits
            int m = receivedData.length();
            int r = 0;
            for (int i = 0; i < m; i++) {
                if (Math.pow(2, i) >= m + i + 1) {
                    r = i;
                    break;
                }
            }

            // Calculate the error position (if any)
            int errorPosition = detectError(receivedData, r);

            // Perform error correction (if errorPosition is not 0)
            if (errorPosition != 0) {
                // Flip the bit at the error position to correct the error
                StringBuilder correctedData = new StringBuilder(receivedData);
                int errorBit = m - errorPosition;
                correctedData.setCharAt(errorBit, correctedData.charAt(errorBit) == '0' ? '1' : '0');
                receivedData = correctedData.toString();
            }

            // Print the result based on error detection and correction
            if (errorPosition == 0) {
                System.out.println("No errors detected in the received message.");
                System.out.println("Received data: " + receivedData);
            } else if (errorPosition > 0) {
                System.out.println("Errors detected in the received message.");
                System.out.println("Discarding the received data due to errors.");
            } else {
                System.out.println("Errors detected and corrected in the received message.");
                System.out.println("Corrected data: " + receivedData);
            }
        }
    }
}
