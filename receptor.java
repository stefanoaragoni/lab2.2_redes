import java.io.IOException;
import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class receptor {

    public static void main(String[] args) {

        Set<String> receivedData = capaTransmision.main();

        for (String data : receivedData) {
            ArrayList<String> arrayEnlace = capaEnlace.main(data);
            
            ArrayList<String> arrayPresentacion = capaPresentacion.main(arrayEnlace);

            capaAplicacion.main(arrayPresentacion);
        }
        
    }
}

class capaTransmision{

    public static Set<String> main() {
        int port = 8080;

        Set<String> receivedData = new HashSet<>();

        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Esperando conexiones entrantes...");

            try (Socket clientSocket = serverSocket.accept()) {
                System.out.println("Conexion entrante de: " + clientSocket.getInetAddress());

                InputStream inputStream = clientSocket.getInputStream();
                byte[] buffer = new byte[1024];

                int bytesRead;
                while ((bytesRead = inputStream.read(buffer)) != -1) {
                    String data = new String(buffer, 0, bytesRead);
                    receivedData.add(data);
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println("\nDatos unicos recibidos:");
        for (String data : receivedData) {
            System.out.println(data);
        }

        return receivedData;
    }

}

class capaEnlace{

    public static ArrayList<String> main(String data) {

        // Preguntar qué metodo de detección de errores se usará
        // 1. Hamming
        // 2. CRC32

        int opcion;

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
            String byteString = trama.substring(i, i + 8);
            int byteInt = Integer.parseInt(byteString, 2);
            char byteChar = (char) byteInt;
            texto += byteChar;
        }

        ArrayList<String> info = new ArrayList<>(List.of(texto, error, metodo));
        return info;
    }
}

class capaAplicacion{

    public static void main(ArrayList<String> data) {
        // Data contiene texto, si se detecto / corrigio error y el metodo usado

        String texto = data.toArray()[0].toString();
        String error = data.toArray()[1].toString();
        String metodo = data.toArray()[2].toString();

        if (metodo == "hamming") {
            System.out.println("\n---------------\nMetodo de correccion de errores: Hamming");

            if (error == "true") {
                System.out.println("-Se detecto un error en la trama recibida, se corrigio y se convirtio a texto.");
                System.out.println("\nTexto recibido (corregido): " + texto);
            }
            else if (error == "false") {
                System.out.println("-No se detectaron errores en la trama recibida, se convirtio a texto.");
                System.out.println("\nTexto recibido: " + texto);
            }
            else {
                System.out.println("-Se detecto más de un error en la trama recibida. No se pudo corregir.");
            }
        }
        else if (metodo == "crc32"){
            System.out.println("\n---------------\nMetodo de deteccion de errores: CRC32");

            if (error == "true") {
                System.out.println("-Se detecto un error en la trama recibida. Se descarto la trama");
            }
            else if (error == "false") {
                System.out.println("-No se detectaron errores en la trama recibida, se convirtio a texto.");
                System.out.println("\nTexto recibido: " + texto);
            }
        }

    }

}

