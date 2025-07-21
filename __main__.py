from caenParser import select_file, Parser
import matplotlib.pyplot as plt


def main():
    dc = Parser()
    dc.set_measure_magnitude("VOLTAGE")  # Set the measure magnitude to ADC_COUNTS
    dc.loadFile(select_file())
    plt.figure(figsize=(10, 6))
    event_id = 1
    
    df = dc.get_data_frame(event_id, 0)
    plt.plot(df["Time"], df["Amplitude"], label=f"Event {event_id}", alpha=0.5)
    plt.title("Channel Data from Events")

    event_id = 2
    df = dc.get_data_frame(event_id, 0)
    plt.plot(df["Time"], df["Amplitude"], label=f"Event {event_id}", alpha=0.5)
    plt.title("Channel Data from Events")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (V)")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()