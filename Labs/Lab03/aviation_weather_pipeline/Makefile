.PHONY: all fetch analyze clean

#Default target
all: analyze

#Fetch precedes analyze
fetch:
	@echo "Starting fetch step..."
	./fetch_metars.sh
	@echo "Fetch step complete. Raw data saved in 'raw_metars/'."

analyze: fetch
	@echo "Starting analysis step..."
	./analyze_data.sh
	@echo "Analysis step complete. Results saved to 'weather_report.csv'."
	@echo "Pipeline completed successfully!"

#Removes entire raw_metars directory
clean:
	@echo "Cleaning up generated files..."
	rm -rf raw_metars weather_report.csv
	@echo "Workspace cleaned."

