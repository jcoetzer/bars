/**
 * @file SsmUtils.hpp
 */
#include "FlightData.h"

/**
 * Trim trailing spaces
 *
 * @param s     input
 * @param t     delimiter
 *
 * @return trimmed string
 */
std::string& rtrim(std::string& s,
                   const char* t = " \t\n\r\f\v");

/**
 * Make path of itenaries or something
 *
 * @param it                          itenary data
 * @param n_it                        number of itenary entries
 *
 * @return text string
 */
char * mk_path(struct IT ** it,
               const int n_it);

/**
 * Get times and terms for marketed from operational flight
 *
 * @param orig              departure
 * @param dest              arrival
 * @param dupfligth         duplicate flight
 * @param it                itenary data
 * @param cur_it            current itenary
 * @param depTerminalSize   departure buffer size
 * @param arrTerminalSize   arrival buffer size
 *
 * @return zero upon success otherwise non-zero
 */
int getTimesTermsForMarketedFromOperational(char *orig,
                                            char *dest,
                                            IT dupfligth,
                                            struct IT ** it,
                                            int cur_it,
                                            size_t depTerminalSize,
                                            size_t arrTerminalSize);