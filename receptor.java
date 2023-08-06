import java.io.IOException;
import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class receptor {

    public static void main(String[] args) {

        String metodo = "";

        if (args.length > 0) {
            metodo = args[0];
        }


        String receivedData = capaTransmision.main();

        ArrayList<String> arrayEnlace = capaEnlace.main(receivedData, metodo);
        
        ArrayList<String> arrayPresentacion = capaPresentacion.main(arrayEnlace);

        capaAplicacion.main(arrayPresentacion);
        
        
    }
}

class capaTransmision {

    public static String main() {
        int port = 8080;

        String receivedData = null;

        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Esperando conexiones entrantes...");

            try (Socket clientSocket = serverSocket.accept()) {
                System.out.println("Conexion entrante de: " + clientSocket.getInetAddress());

                InputStream inputStream = clientSocket.getInputStream();
                byte[] buffer = new byte[1024];

                int bytesRead;
                if ((bytesRead = inputStream.read(buffer)) != -1) {
                    receivedData = new String(buffer, 0, bytesRead);
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println("\nDato recibido: " + receivedData);
        return receivedData;
    }

    public static void main(String[] args) {
        main();
    }
}


class capaEnlace{

    public static ArrayList<String> main(String data, String metodo) {

        // Preguntar qué metodo de detección de errores se usará
        // 1. Hamming
        // 2. CRC32

        int opcion;

        if (metodo.isEmpty()) {
            System.out.println("\nElija el metodo de deteccion de errores:");
            System.out.println("1. Hamming");
            System.out.println("2. CRC32");

            while (true) {
                try {
                    opcion = Integer.parseInt(System.console().readLine("Opcion: "));
                    if (opcion == 1 || opcion == 2) {
                        break;
                    }
                } catch (NumberFormatException e) {
                    System.out.println("Opcion invalida.");
                }
            }
        
        } else{
            opcion = Integer.parseInt(metodo);

        }   


        if (opcion == 1) {
            ArrayList<String> hamming = Hamming_Receptor.main(data);
            return hamming;
        }
        else {
            ArrayList<String> crc32 = crc32_receptor.main(data);
            return crc32;
        }

    }

}

class capaPresentacion{

    public static ArrayList<String> main(ArrayList<String> data) {
        // Data contiene trama, si se detecto / corrigio error y el metodo usado

        String trama = data.toArray()[0].toString();
        String error = data.toArray()[1].toString();
        String metodo = data.toArray()[2].toString();

        System.out.println("\nIntentando decodificar trama recibida: " + trama);

        // Convertir la trama a texto
        String texto = "";

        for (int i = 0; i < trama.length(); i += 8) {
            int endIndex = Math.min(i + 8, trama.length());
            String byteString = trama.substring(i, endIndex);
            int byteInt = Integer.parseInt(byteString, 2);
            char byteChar = (char) byteInt;
            texto += byteChar;
        }


        ArrayList<String> info = new ArrayList<>(List.of(texto, error, metodo));
        return info;
    }
}

class capaAplicacion {

    public static void main(ArrayList<String> data) {
        String texto = data.get(0);
        String error = data.get(1);
        String metodo = data.get(2);
        
        StringBuilder logMessage = new StringBuilder();


        if (metodo.equals("hamming")) {
            logMessage.append("\n---------------\nMetodo de correccion de errores: Hamming");

            if (error.equals("true")) {
                logMessage.append("\n-Se detecto un error en la trama recibida, se corrigio y se convirtio a texto.");
                logMessage.append("\nTexto recibido (corregido): ").append(texto);
                guardarEnArchivo(metodo, "corrected");
            } else if (error.equals("false")) {
                logMessage.append("\n-No se detectaron errores en la trama recibida, se convirtio a texto.");
                logMessage.append("\nTexto recibido: ").append(texto);
                guardarEnArchivo(metodo, "clean");
            } else {
                logMessage.append("\n-Se detecto más de un error en la trama recibida. No se pudo corregir.");
                guardarEnArchivo(metodo, "error");
            }
        } else if (metodo.equals("crc32")) {
            logMessage.append("\n---------------\nMetodo de deteccion de errores: CRC32");

            if (error.equals("true")) {
                logMessage.append("\n-Se detecto un error en la trama recibida. Se descarto la trama");
                guardarEnArchivo(metodo, "error");
            } else if (error.equals("false")) {
                logMessage.append("\n-No se detectaron errores en la trama recibida, se convirtio a texto.");
                logMessage.append("\nTexto recibido: ").append(texto);
                guardarEnArchivo(metodo, "clean");
            }
        }

        System.out.println(logMessage);
    }

    private static void guardarEnArchivo(String metodo, String estado) {
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter(metodo + ".txt", true));
            writer.append(estado).append("\n");
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

