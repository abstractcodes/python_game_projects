import javafx.animation.Animation;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.chart.CategoryAxis;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import javafx.util.Duration;

public class TaskManagementTool extends Application {

    private ObservableList<String> tasks = FXCollections.observableArrayList();
    private Timeline timeline;
    private int seconds = 1500; // 1500 seconds = 25 minutes
    private boolean isRunning = false;
    private XYChart.Series<String, Number> series = new XYChart.Series<>();

    @Override
    public void start(Stage primaryStage) {
        ListView<String> taskList = new ListView<>(tasks);
        taskList.setPrefHeight(200);

        TextField taskField = new TextField();
        taskField.setPromptText("Enter new task");

        Button addButton = new Button("Add");
        addButton.setOnAction(event -> {
            String newTask = taskField.getText();
            if (!newTask.isEmpty()) {
                tasks.add(newTask);
                taskField.clear();
            }
        });

        Button deleteButton = new Button("Delete");
        deleteButton.setOnAction(event -> {
            String selectedTask = taskList.getSelectionModel().getSelectedItem();
            if (selectedTask != null) {
                tasks.remove(selectedTask);
            }
        });

        HBox buttons = new HBox(10, addButton, deleteButton);
        buttons.setAlignment(Pos.CENTER);

        Label timerLabel = new Label("25:00");
        timerLabel.setStyle("-fx-font-size: 40pt; -fx-font-weight: bold;");

        Button startButton = new Button("Start");
        startButton.setOnAction(event -> {
            if (!isRunning) {
                startTimer(timerLabel);
                startButton.setText("Pause");
            } else {
                pauseTimer();
                startButton.setText("Start");
            }
            isRunning = !isRunning;
        });

        HBox timerBox = new HBox(10, timerLabel, startButton);
        timerBox.setAlignment(Pos.CENTER);

        CategoryAxis xAxis = new CategoryAxis();
        xAxis.setLabel("Tasks");
        NumberAxis yAxis = new NumberAxis();
        yAxis.setLabel("Time Spent (hours)");
        LineChart<String, Number> lineChart = new LineChart<>(xAxis, yAxis);
        lineChart.setTitle("Time Spent on Tasks");
        lineChart.getData().add(series);

        Button updateButton = new Button("Update Graph");
        updateButton.setOnAction(event -> {
            series.getData().clear();
            for (String task : tasks) {
                series.getData().add(new XYChart.Data<>(task, Math.random() * 24)); // Replace with actual time spent
            }
        });

        VBox root = new VBox(10, taskList, taskField, buttons, timerBox, lineChart, updateButton);
        root.setPadding(new Insets(10));

        Scene scene = new Scene(root, 800, 600);
        primaryStage.setTitle("Task Management Tool");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    private void startTimer(Label timerLabel) {
        timeline = new Timeline(new KeyFrame(Duration.seconds(1), event -> {
            seconds--;
            timerLabel.setText(String.format("%02d:%02d", seconds / 60, seconds % 60));
            if (seconds == 0) {
                timeline.stop();
            }
        }));
        timeline.setCycleCount(Animation.INDEFINITE);
        timeline.play();
    }

    private void pauseTimer() {
        timeline.stop();
    }

    public static void main(String[] args) {
        launch(args);
    }
}