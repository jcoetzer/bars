/**
 * @file SsmDate.hpp
 *
 * Read date in any format and convert
 */
#ifndef SSMDATE_HPP
#define SSMDATE_HPP

#include <string>

/**
 * @class SsmDate
 *
 * Date in IATA or MDY format
 */
class SsmDate
{
public:
    /**
     * Constructor
     *
     * @param adate     date in numeric format
     */
    SsmDate(long adate);

    /**
     * Constructor
     *
     * @param adate     date in MDY format
     */
    SsmDate(char * adate);

    /**
     * Constructor
     *
     * @param datev     date in whatever format
     */
    SsmDate(std::string datev);

    /**
     * Destructor
     */
    ~SsmDate();

    char iatal[16];              ///< IATA format date with 4-digit year e.g. 20JAN2018
    char iata[16];              ///< IATA format date e.g. 20JAN18
    char mdy[16];               ///< MDY format date e.g. 04/20/2018
    char iso[16];               ///< YMD format date e.g. 2018-04-20
    int dow;                    ///< Day of week : Monday=1...Sunday=7
};

#endif // SSMDATE_HPP
