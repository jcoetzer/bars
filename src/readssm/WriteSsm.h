/**
 * @file WriteSsm.h
 *
 * Write SSM message
 */
#ifndef WRITESSM_H
#define WRITESSM_H

#include <string>
#include <time.h>

/**
 * @class WriteSsmData
 *
 * SSM data storage
 */
class WriteSsmData
{
public:
    /**
     * Constructor
     *
     * @param aftype                 file type
     * @param aAddress              origin address
     * @param aSender               sender address
     * @param aTimeMode             time mode, local or UTC
     * @param aFlightNumber         flight number
     * @param aFlightDateStart      start date
     * @param aFlightDateEnd        end date
     * @param aDepartCity           departure airport
     * @param aDepartTime           departure time
     * @param aArriveCity           arrival airport
     * @param aArriveTime           arrival time
     * @param aAircraftCode         aircraft code
     * @param aFrequencyCode        day of week frequency code
     * @param aCodeshare            codeshare flight number
     * @param aTailNumber           tail number
     */
    WriteSsmData(std::string aftype,
                 std::string aAddress,
                 std::string aSender,
                 std::string aTimeMode,
                 std::string aFlightNumber,
                 std::string aFlightDateStart,
                 std::string aFlightDateEnd,
                 std::string aDepartCity,
                 int aDepartTime,
                 std::string aArriveCity,
                 int aArriveTime,
                 std::string aAircraftCode,
                 int aFrequencyCode,
                 std::string aCodeshare,
                 std::string aTailNumber);

    /**
     * Destructor
     */
    ~WriteSsmData();

    /**
     * Write cancel SSM
     */
    void WriteCnl();

    /**
     * Write equipment SSM
     */
    void WriteEqt();

    /**
     * Write new flight SSM
     */
    void WriteNew();

    /**
     * Write replace flight SSM
     */
    void WriteRpl();

    /**
     * Write time change SSM
     */
    void WriteTim();

    /**
     * Generate file name
     *
     * @return file name
     */
    std::string FileName();

    /**
     * Write SSM file
     *
     * @param ofname    output file name
     *
     * @return zero upon success otherwise non-zero
     */
    int WriteSsmFile(std::string ofname);

    std::string ftype;               ///< file type i.e. NEW, CNL, TIM or EQT
    std::string Address;             ///< origin address
    std::string Sender;              ///< sender address
    std::string TimeMode;            ///< time mode - local or UTC
    std::string FlightNumber;        ///< flight number
    std::string FlightDateStart;     ///< start date
    std::string FlightDateEnd;       ///< end date
    std::string DepartCity;          ///< departure airport
    std::string DepartTime;          ///< departure time
    std::string ArriveCity;          ///< arrival airport
    std::string ArriveTime;          ///< arrival time
    std::string AircraftCode;        ///< aircraft configuration code
    std::string FrequencyCode;       ///< frequency code
    std::string Codeshare;           ///< codeshare flight number

private:
    FILE * ofile;               ///< file handle
    char date1[16];             ///< start date
    char date2[16];             ///< end date
    std::string SeatCount;           ///< number of seats
    std::string BookingClasses;      ///< booking classes
    std::string TailNumber;          ///< aircraft tail number

    time_t now;                 ///< current time number
    struct tm *nowstruct;       ///< current time structure
    char timenow[16];           ///< current time buffer

    std::string obuff;               ///< output buffer
};

#endif // WRITESSM_H


